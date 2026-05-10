import React, {
  useEffect,
  useRef
} from "react";

import { Timeline } from "vis-timeline/standalone";
import { DataSet } from "vis-data";

import "vis-timeline/styles/vis-timeline-graph2d.min.css";
import "./timeline.css";

function TimelineView({ timelineData }) {

  const timelineRef = useRef(null);

  useEffect(() => {

    if (!timelineData || timelineData.length === 0) {
      return;
    }

    const items = new DataSet(
      timelineData.map((event, index) => {

        // -----------------------------
        // EVENT LABEL
        // -----------------------------

        let label = event.event_type;

        if (event.event_type === "flight_start") {
          label = "Flight Start";
        }

        else if (event.event_type === "flight_end") {
          label = "Flight End";
        }

        else if (event.event_type === "image_capture") {
          label = "Image Captured";
        }

        else if (event.event_type === "video_recorded") {
          label = "Video Recorded";
        }

        else if (event.event_type === "home_point") {
          label = "Home Point";
        }

        else if (event.event_type === "account_detected") {
          label = "DJI Account";
        }

        // -----------------------------
        // COLOR CLASSES
        // -----------------------------

        let className = "defaultEvent";

        if (event.event_type === "flight_start") {
          className = "flightStart";
        }

        else if (event.event_type === "flight_end") {
          className = "flightEnd";
        }

        else if (event.event_type === "image_capture") {
          className = "imageEvent";
        }

        else if (event.event_type === "video_recorded") {
          className = "videoEvent";
        }

        else if (event.event_type === "home_point") {
          className = "homeEvent";
        }

        else if (event.event_type === "account_detected") {
          className = "accountEvent";
        }

        // -----------------------------
        // RETURN ITEM
        // -----------------------------

        return {

          id: index + 1,

          content: label,

          start: event.timestamp,

          title: `
            ${event.description || ""}
            ${event.filename || ""}
          `,

          className: className

        };

      })
    );

    const options = {

      stack: true,

      zoomable: true,

      moveable: true,

      selectable: true,

      tooltip: {
        followMouse: true
      },

      orientation: "top",

      height: "250px"

    };

    const timeline = new Timeline(
      timelineRef.current,
      items,
      options
    );

    return () => {
      timeline.destroy();
    };

  }, [timelineData]);

  return (
    <div
      ref={timelineRef}
      style={{
        background: "white",
        borderRadius: "10px",
        padding: "10px"
      }}
    />
  );
}

export default TimelineView;