import React, { useState } from "react";
import { IonRow, IonCol, IonCard, IonCardContent } from "@ionic/react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";
import "../pages/Home.css";
interface Post {
  caption: string;
  id: string;
  media_type: string;
  media_url: string;
  username: string;
  score: number;
  message: string;
}

const PostComponent: React.FC<{ post: Post }> = ({ post }) => {
  const [expanded, setExpanded] = useState(false);

  const handleToggleExpand = () => {
    setExpanded(!expanded);
  };

  const renderCaption = () => {
    const maxLength = 50; // Adjust the character limit as needed

    if (post.caption.length <= maxLength || expanded) {
      return (
        <h3 className="post-caption">
          {post.caption}
          {post.caption.length > maxLength ? (
            <span className="read-more" onClick={handleToggleExpand}>
              {expanded ? "...Read Less" : "...Read More"}
            </span>
          ) : (
            <></>
          )}
        </h3>
      );
    } else {
      return (
        <>
          <h3 className="post-caption">
            {post.caption.substring(0, maxLength)}...
            <span className="read-more" onClick={handleToggleExpand}>
              {expanded ? "Read Less" : "Read More"}
            </span>
          </h3>
        </>
      );
    }
  };

  const textCenter = {
    id: "textCenter",
    beforeDatasetsDraw(chart: any, args: any, pluginOptions: any) {
      const { ctx, data } = chart;
      ctx.save();
      ctx.font = "bolder 12px";
      ctx.fillStyle = "rgba(255, 99, 132, 1)";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(
        `${data.datasets[0].data[0]}`,
        chart.getDatasetMeta(0).data[0].x,
        chart.getDatasetMeta(0).data[0].y
      );
    },
  };

  return (
    <IonCard>
      <IonCardContent>
        <IonRow>
          <IonCol size="5" className="doughnut-col">
            <Doughnut
              data={{
                labels: [],
                datasets: [
                  {
                    data: [post.score * -100, 100 - post.score * -100],
                    backgroundColor: [
                      "rgba(255,74,74, 0.7)",
                      "rgba(188,190,192, 0.7)",
                    ],
                    borderColor: [
                      "rgba(255,74,74, 1)",
                      "rgba(188,190,192, 1)",
                    ],
                    borderWidth: 0.5,
                  },
                ],
              }}
              plugins={[textCenter]}
            ></Doughnut>
          </IonCol>
          <IonCol size="7" className="sadness-text-column">
            <div className="sadness-details">
              <h3 className="post-sadness-text">Sadness</h3>
              <span className="score-text">{post.score * -100}%</span>
              <h3 className="post-sadness-text">Status</h3>
              <span className="sadness-message">{post.message}</span>
            </div>
          </IonCol>
        </IonRow>
        <IonRow>
          <IonCol className="caption-column">{renderCaption()}</IonCol>
        </IonRow>
      </IonCardContent>
    </IonCard>
  );
};

export default PostComponent;
