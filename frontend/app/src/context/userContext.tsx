import { createContext, useState, useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import AuthContext from "./authContext";

interface UserProviderProps {
  children: React.ReactNode;
}

interface UserContextProps {
    getUserPosts: any;
    userPosts: any;
    getSadnessScores: any;
}

interface Post {
    caption: string;
    id: string;
    media_type: string;
    media_url: string;
    username: string;
    score: any;
    message: any;
  }

const UserContext = createContext<UserContextProps | undefined>(undefined);

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {

  const history = useHistory();

  const [userPosts, setUserPosts] = useState<Post[]>([]);

  const authContext = useContext(AuthContext)!;
  const {
    getUserId,
    getAccessToken,
  } = authContext;

  const getUserPosts = async () => {
    await axios.post('http://127.0.0.1:8000/instagram-api/get-user-posts/',{
        user_id: getUserId(),
        access_token: getAccessToken()
    })
    .then((resp)=>{
        var response = resp.data.response.data;
        getSadnessScores({'posts':response})
    })
    .catch((error) => console.error(error));
  }

  const getSadnessScores = async (posts: any) =>{
    await axios.post("http://127.0.0.1:8000/emotion-analyzer/getBulkSadnessScore/",posts).then((resp)=>{
        var response = resp;
        setUserPosts(response.data.posts);
    })
    .catch((error) => console.error(error));
  }

  return (
    <UserContext.Provider
      value={{
        userPosts,
        getUserPosts,
        getSadnessScores,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;
