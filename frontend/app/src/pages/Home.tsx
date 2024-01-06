import {
  IonButton,
  IonCard,
  IonCardContent,
  IonCol,
  IonContent,
  IonGrid,
  IonHeader,
  IonPage,
  IonRefresher,
  IonRefresherContent,
  IonRow,
  IonTitle,
  IonToolbar,
  RefresherEventDetail,
} from "@ionic/react";
import "./Home.css";

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";

import React, { useState, useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";
import AuthContext from "../context/authContext";
import UserContext from "../context/userContext";
import PostComponent from "../components/postComponent";

interface Post {
  caption: string;
  id: string;
  media_type: string;
  media_url: string;
  username: string;
  score: any;
  message: any;
}

ChartJS.register(ArcElement, Tooltip, Legend);

const Home: React.FC = () => {
  const history = useHistory();

  const authContext = useContext(AuthContext)!;
  const userContext = useContext(UserContext)!;

  const [posts, setPosts] = useState<Post[]>([]);

  const {
    authorizationLink,
    isAuthenticated,
    checkAuthentication,
    generateAuthCode,
    generateAccessToken,
  } = authContext;

  const { getUserPosts, userPosts, getSadnessScores } = userContext;

  useEffect(() => {
    if (!checkAuthentication()) {
      history.push("/authorization");
    }
  }, []);

  useEffect(() => {
    getUserPosts();
  }, []);

  function handleRefresh(event: CustomEvent<RefresherEventDetail>) {
    setTimeout(() => {
      if(checkAuthentication()){
        getUserPosts();
      }
      else{
        history.push("/authorization");
      }
      event.detail.complete();
    }, 2000);
  }

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>How Sad are you?</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent class="ion-padding">
        <IonRefresher slot="fixed" onIonRefresh={handleRefresh}>
          <IonRefresherContent>
          </IonRefresherContent>
        </IonRefresher>
        <IonGrid>
              {userPosts &&
                userPosts.map((post: Post) => (
                  <IonRow key={post.id}>
                    <IonCol size="12" size-sm="8" size-md="6" size-lg="4">
                      <PostComponent post={post}></PostComponent>
                    </IonCol>
                  </IonRow>
                ))}
            </IonGrid>
      </IonContent>
    </IonPage>
  );
};

export default Home;
