import { useState } from 'react';
import { Button, Typography, CircularProgress, Card, CardContent, Grid, Box, Paper } from '@mui/material';

const TrainModel = () => {
  const [trainingResults, setTrainingResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const trainModel = async () => {
    setLoading(true);
    const response = await fetch('/api/train', { method: 'POST' });
    const data = await response.json();

    if (response.status === 200) {
      setTrainingResults(data); // Save the full response data
    } else {
      setTrainingResults('Training failed. Check logs.');
    }
    setLoading(false);
  };

  return (
    <Box sx={{ width: '100%', padding: 3 }}>
      <Typography variant="h4" gutterBottom align="center" color="primary">
        Train the Model (KDD-Cup Dataset)
      </Typography>

      <Grid container spacing={3} justifyContent="center">
        {/* Start Training Button */}
        <Grid item>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={trainModel}
            disabled={loading}
            sx={{ minWidth: 200 }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Start Training'}
          </Button>
        </Grid>

        {/* Display Results */}
        {trainingResults && (
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="textPrimary" gutterBottom>
                  Training Results
                </Typography>

                {/* Accuracy Display */}
                <Paper sx={{ padding: 2, marginBottom: 2, backgroundColor: '#f5f5f5' }}>
                  <Typography variant="h6" color="textSecondary">Accuracy</Typography>
                  <Typography variant="h4" color="primary">{trainingResults.accuracy}</Typography>
                </Paper>

                {/* Sniffed Packets */}
                <Typography variant="h6" color="textSecondary">Sniffed Packets</Typography>
                <Grid container spacing={2}>
                  {trainingResults.sniffed_packets.map((packet, index) => (
                    <Grid item xs={6} sm={4} key={index}>
                      <Card sx={{ padding: 2, boxShadow: 3 }}>
                        <Typography variant="body1" color={packet === 'normal.' ? 'green' : 'red'}>
                          {packet}
                        </Typography>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default TrainModel;
