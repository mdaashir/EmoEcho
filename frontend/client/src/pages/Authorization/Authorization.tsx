import {
  IonContent,
  IonPage,
  IonButton,
  IonCol,
  IonGrid,
  IonRow,
  IonCard,
  IonCardContent,
} from "@ionic/react";

import "./Authorization.css";

import React, { useState, useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";

import AuthContext from "../../context/authContext";

const Authorization: React.FC = () => {
  const history = useHistory();

  const authContext = useContext(AuthContext)!;
  const {
    authorizationLink,
    isAuthenticated,
    checkAuthentication,
    generateAuthCode,
    generateAccessToken,
  } = authContext;

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    if (code && code?.length > 0) {
      generateAccessToken(code);
    } else {
      generateAuthCode();
    }
  }, [authorizationLink]);

  useEffect(() => {
    if (checkAuthentication()) {
      history.push("/home");
    }
  }, []);

  useEffect(() => {
    if (checkAuthentication()) {
      history.push("/home");
    }
  }, [isAuthenticated]);

  const handleAuthorize = () => {
    if (authorizationLink && authorizationLink.length > 0) {
      window.location.replace(authorizationLink);
    }
    else{
      generateAuthCode();
    }
  };

  return (
    <IonPage>
      <IonContent class="ion-padding">
        <IonGrid>
          <IonRow class="authorize-row">
            <IonCol size="12" size-sm="8" size-md="6" size-lg="4">
              <IonCard color="dark">
                <IonCardContent>
                  <IonRow>
                    <strong className="app-name">How Sad Are You?</strong>
                  </IonRow>
                  <IonRow>
                    <ul className="app-notice-text">
                      <li>
                        This app requires permission to connect with your
                        Instagram profile in order to obtain your profile
                        information and posts.
                      </li>
                      <li>
                        Please tap the 'Authorize' button to grant the necessary
                        permissions and allow this app to interact with your
                        Instagram account.
                      </li>
                    </ul>
                  </IonRow>
                  <IonRow>
                    <IonButton onClick={handleAuthorize} size="small">
                      Authorize with Instagram
                    </IonButton>
                  </IonRow>
                </IonCardContent>
              </IonCard>
            </IonCol>
          </IonRow>
        </IonGrid>
      </IonContent>
    </IonPage>
  );
};

export default Authorization;
