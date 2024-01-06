import { createContext, useState, useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

interface AuthProviderProps {
  children: React.ReactNode;
}

interface AuthContextProps {
  authorizationLink: string;
  isAuthenticated: boolean;
  checkAuthentication: any;
  generateAuthCode: any;
  generateAccessToken: any;
  getUserId: any;
  getAccessToken: any;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const history = useHistory();

  const [authorizationLink, setAuthorizationLink] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const redirect_uri = "<YOUR_REDIRECT_URI>";
  const client_id = "<YOUR_CLIENT_ID>";
  const client_secret = "<YOUR_CLIENT_SECRET>";

  const generateAuthCode = async () => {
    await axios
      .post("http://127.0.0.1:8000/instagram-api/get-authorization-code/", {
        client_id: client_id,
        redirect_uri: redirect_uri,
        scope: "user_profile,user_media",
        response_type: "code",
      })
      .then((resp) => {
        var authLink = resp.data.response;
        setAuthorizationLink(authLink);
      })
      .catch((error) => console.error(error));
  };

  const generateAccessToken = async (code: string) => {
    await axios
      .post("http://127.0.0.1:8000/instagram-api/get-access-token/", {
        client_id: client_id,
        client_secret: client_secret,
        grant_type: "authorization_code",
        redirect_uri: redirect_uri,
        code: code,
      })
      .then((resp) => {
        var response = resp.data;
        saveObjectToLocalStorage("token", response);
        setIsAuthenticated(true);
      })
      .catch((error) => console.error(error));
  };

  const checkAuthentication = () => {
    if (getObjectFromLocalStorage("token")) {
      setIsAuthenticated(true);
      return true;
    } else {
      setIsAuthenticated(false);
      return false;
    }
  };

  const saveObjectToLocalStorage = (key: string, object: any) => {
    try {
      const serializedObject = JSON.stringify(object);
      localStorage.setItem(key, serializedObject);
    } catch (error) {
      console.error("Error saving to local storage:", error);
    }
  };

  const getObjectFromLocalStorage = (key: string) => {
    try {
      const serializedObject = localStorage.getItem(key);
      return serializedObject ? JSON.parse(serializedObject) : null;
    } catch (error) {
      console.error("Error retrieving from local storage:", error);
      return null;
    }
  };

  const getUserId = () => {
    const token = getObjectFromLocalStorage("token");
    return token.user_id;
  };

  const getAccessToken = () => {
    const token = getObjectFromLocalStorage("token");
    return token.access_token;
  };

  return (
    <AuthContext.Provider
      value={{
        authorizationLink,
        isAuthenticated,
        checkAuthentication,
        generateAuthCode,
        generateAccessToken,
        getUserId,
        getAccessToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
