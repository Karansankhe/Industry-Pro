import React, { useState } from 'react';
import { Container, TextField, Button, MenuItem, Typography, Paper, Box } from '@mui/material';
import axios from 'axios';

function App() {
  const [symbol, setSymbol] = useState('');
  const [source, setSource] = useState('yahoo_finance');
  const [stockData, setStockData] = useState(null);
  const [analysis, setAnalysis] = useState('');
  const [geminiResponse, setGeminiResponse] = useState('');

  const handleFetchData = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/fetch_stock_data?symbol=${symbol}&source=${source}`);
      setStockData(response.data.stock_data);
      setAnalysis(response.data.analysis);
      setGeminiResponse(response.data.gemini_response);
    } catch (error) {
      console.error("Error fetching stock data:", error);
      setStockData(null);
      setAnalysis('');
      setGeminiResponse('');
    }
  };

  const renderStockData = () => {
    if (!stockData) return null;
    return (
      <Paper style={{ padding: '16px', marginTop: '16px' }}>
        <Typography variant="h6">Stock Data</Typography>
        <pre>{JSON.stringify(stockData, null, 2)}</pre>
      </Paper>
    );
  };

  const renderAnalysis = () => {
    if (!analysis) return null;
    return (
      <Paper style={{ padding: '16px', marginTop: '16px' }}>
        <Typography variant="h6">Analysis</Typography>
        <Typography>{analysis}</Typography>
      </Paper>
    );
  };

  const renderGeminiResponse = () => {
    if (!geminiResponse) return null;
    return (
      <Paper style={{ padding: '16px', marginTop: '16px' }}>
        <Typography variant="h6">Gemini AI Response</Typography>
        <Typography>{geminiResponse}</Typography>
      </Paper>
    );
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Stock Information</Typography>
      <TextField
        label="Stock Symbol"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        select
        label="Data Source"
        value={source}
        onChange={(e) => setSource(e.target.value)}
        fullWidth
        margin="normal"
      >
        <MenuItem value="alpha_vantage">Alpha Vantage</MenuItem>
        <MenuItem value="yahoo_finance">Yahoo Finance</MenuItem>
      </TextField>
      <Button variant="contained" color="primary" onClick={handleFetchData} fullWidth>Fetch Data</Button>

      <Box mt={2}>
        {renderStockData()}
        {renderAnalysis()}
        {renderGeminiResponse()}
      </Box>
    </Container>
  );
}

export default App;
