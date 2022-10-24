import "./App.css";
import PropsExample from "./PropsExample";
import StateExample from "./StateExample";
import FetchAPI from "./FetchAPI";
import FetchAPIMultipleImages from "./FetchAPIMultipleImages";

function App() {
  return (
    <div className="App">
      Hello
      <PropsExample name="Dave" age={40} />
      <StateExample />
      {/* <FetchAPI /> */}
      <FetchAPIMultipleImages />
    </div>
  );
}

export default App;
