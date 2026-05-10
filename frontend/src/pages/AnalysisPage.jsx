import TimelineView from "../components/TimelineView";
const [timelineData, setTimelineData] = useState([]);

useEffect(() => {

  async function loadTimeline() {

    try {

      const analysisPath =
        `${currentCasePath}/analysis/timeline.json`;

      const response = await fetch(
        `file://${analysisPath}`
      );

      const data = await response.json();

      setTimelineData(data);

    }
    catch (err) {

      console.error(err);

    }

  }

  loadTimeline();

}, []);

<div style={{ marginTop: "20px" }}>

  <h2>Timeline Reconstruction</h2>

  <TimelineView timelineData={timelineData} />

</div>