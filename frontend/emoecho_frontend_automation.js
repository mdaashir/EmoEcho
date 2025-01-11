import { exec, spawn } from 'child_process';
import { existsSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory and filename
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Utility to run shell commands
function runCommand(command, options = {}) {
	return new Promise((resolve, reject) => {
		const process = exec(command, options, (error, stdout, stderr) => {
			if (error) {
				reject(stderr.trim() || stdout.trim() || error.message);
			} else {
				resolve(stdout.trim());
			}
		});

		process.stdout.on('data', (data) => console.log(data.toString()));
		process.stderr.on('data', (data) => console.error(data.toString()));
	});
}

// Utility to log errors and exit
function errorExit(message) {
	console.error(`Error: ${message}`);
	process.exit(1);
}

// Check for npm installation
async function checkNpm() {
	try {
		await runCommand('npm --version');
		console.log('npm is installed.');
	} catch (error) {
		errorExit('npm is not installed. Install it from https://nodejs.org/');
	}
}

// Install npm dependencies if `node_modules` is missing
async function installDependencies() {
	if (!existsSync('./node_modules')) {
		console.log('Installing project dependencies...');
		await runCommand('npm install');
		console.log('Dependencies installed successfully.');
	} else {
		console.log('Dependencies are already installed.');
	}
}

// Load and validate environment variables (after checking for node_modules)
async function loadEnvVars() {
	try {
        const dotenv = await import( 'dotenv' );
        const envPath = path.join( __dirname, '../.env' );
        if ( !existsSync( envPath ) )
        {
            console.log( 'No .env file found.' );
        }
		dotenv.config({path: envPath});
	} catch (error) {
		errorExit(
			'dotenv is not installed. Ensure all dependencies are installed or add dotenv to your package.json.'
		);
	}

	const { FRONTEND_PORT, NGROK_AUTH_TOKEN, NGROK_SUBDOMAIN } = process.env;

	if (!FRONTEND_PORT) {
		errorExit(
			'PORT is not set in the .env file. Add PORT=<port_number> to your .env file.'
		);
	}

	console.log(`Using PORT=${FRONTEND_PORT} for the development server.`);
	return { FRONTEND_PORT, NGROK_AUTH_TOKEN, NGROK_SUBDOMAIN };
}

// Create symbolic link for `client/node_modules` to `node_modules`
async function createSymlink() {
	const targetPath = path.join(__dirname, 'node_modules');
	const symlinkPath = path.join(__dirname, 'client', 'node_modules');

	if (!existsSync(symlinkPath)) {
		console.log(
			'Creating symbolic link for shared node_modules in the client folder...'
		);

		if (process.platform === 'win32') {
			await runCommand(
				`cmd /c mklink /D "${symlinkPath}" "${targetPath}"`
			).catch(() =>
				errorExit(
					'Failed to create symbolic link on Windows. Try running as Administrator.'
				)
			);
		} else {
			await runCommand(`ln -s "${targetPath}" "${symlinkPath}"`, {
				shell: true,
			}).catch(() =>
				errorExit('Failed to create symbolic link on Linux/macOS.')
			);
		}

		console.log(
			`Symbolic link created: './client/node_modules' -> '../node_modules'`
		);
	} else {
		console.log("Symbolic link already exists: './client/node_modules'.");
	}
}

// Start the development server
function startDevServer(port) {
	console.log(`Starting the frontend development server on PORT=${port}...`);

	const devServer = spawn('npm', ['run', 'dev', '--', `--port=${port}`], {
		stdio: 'inherit', // Pass stdout/stderr to the parent process
		shell: true, // Ensures compatibility on Windows
	});

	devServer.on('error', (error) => errorExit(error.message));

	process.on('exit', () => {
		console.log('\nStopping the development server...');
		devServer.kill();
	});

	console.log('Development server is running.');
	return devServer;
}

// Check for ngrok and apply configuration if necessary
async function configureNgrok(ngrokAuthToken) {
	try {
		await runCommand('npx ngrok version');
		if (ngrokAuthToken) {
			console.log('Configuring ngrok with the provided authtoken...');
			await runCommand(`npx ngrok authtoken ${ngrokAuthToken}`);
			console.log('ngrok authenticated successfully.');
		} else {
			console.log(
				'No ngrok authtoken provided. You can add it to your .env file for authentication.'
			);
		}
	} catch (error) {
		errorExit(
			"ngrok is not installed. Install it globally using 'npm install -g ngrok'."
		);
	}
}

// Start ngrok tunnel
async function startNgrokTunnel(port, ngrokSubdomain) {
	console.log(
		`Starting ngrok tunnel for the development server on PORT=${port} ...`
	);

	try {
		const ngrokCommand = ngrokSubdomain
			? `npx ngrok http --url=${ngrokSubdomain} ${port}`
			: `npx ngrok http ${port}`;

		console.log(
			ngrokSubdomain
				? `Using custom subdomain: ${ngrokSubdomain}`
				: 'Using a random subdomain...'
		);
		await runCommand(ngrokCommand);
	} catch (error) {
		errorExit('Failed to start ngrok tunnel: ' + error);
	}
}

// Main function to orchestrate the workflow
async function main() {
	// Step 1: Check for npm installation
	await checkNpm();

	// Step 2: Install dependencies
	await installDependencies();

	// Step 3: Dynamically load environment variables
	const { FRONTEND_PORT, NGROK_AUTH_TOKEN, NGROK_SUBDOMAIN } = await loadEnvVars();

	// Step 4: Create symbolic link
	await createSymlink();

	// Step 5: Start the development server
	const devServer = startDevServer(FRONTEND_PORT);

	// Step 6: Configure ngrok if necessary
	await configureNgrok(NGROK_AUTH_TOKEN);

	// Step 7: Start the ngrok tunnel
	await startNgrokTunnel(FRONTEND_PORT, NGROK_SUBDOMAIN);

	// Cleanup the development server on `Ctrl+C` or process termination
	process.on('SIGINT', () => {
		console.log('\nStopping all processes...');
		devServer.kill();
		process.exit(0);
	});
}

// Invoke the main function
main().catch((error) => errorExit(error));
