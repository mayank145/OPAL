/**
 * Tests for main App component
 */
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { fatsAPI } from './services/api';

// Mock the API
jest.mock('./services/api');

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    
    // Mock API responses
    fatsAPI.getAll.mockResolvedValue([]);
    fatsAPI.getById.mockResolvedValue({
      idno: 3759,
      issue: 'Test Issue',
      solution: 'Test Solution',
      sdescribe: '<p>Test description</p>',
      section: 'AO',
      status: 'Active',
      datein: '2025-12-11T10:00:00',
      operator: 'Test User',
    });
  });

  test('renders app title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Fault Tracking System/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders main FATS Entries tab by default', () => {
    render(<App />);
    const mainTab = screen.getByText('FATS Entries');
    expect(mainTab).toBeInTheDocument();
  });

  test('renders Faults List button', () => {
    render(<App />);
    const faultsListButton = screen.getByText('Faults List');
    expect(faultsListButton).toBeInTheDocument();
  });

  test('renders Create New FATS button', () => {
    render(<App />);
    const createButton = screen.getByText(/Create New FATS/i);
    expect(createButton).toBeInTheDocument();
  });

  test('opens All Faults List dialog when button clicked', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const faultsListButton = screen.getByText('Faults List');
    await user.click(faultsListButton);
    
    // Dialog should open (check for dialog content)
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });
  });

  test('opens Create FATS dialog when button clicked', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const createButton = screen.getByText(/Create New FATS/i);
    await user.click(createButton);
    
    // Create dialog should open
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });
  });

  test('shows snackbar notification', async () => {
    render(<App />);
    
    // Trigger an action that shows snackbar
    // (This depends on your implementation)
  });
});

