import TrainModel from './TrainModel';
import PredictPacket from './PredictPacket';

const Dashboard = () => {
  return (
    <div>
      <h1>Network Traffic Analysis Dashboard</h1>
      <TrainModel />
      <hr />
      <PredictPacket />
    </div>
  );
};

export default Dashboard;
