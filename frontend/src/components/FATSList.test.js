/**
 * Tests for FATSList component
 */
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FATSList from './FATSList';
import { fatsAPI, referenceAPI } from '../services/api';

// Mock the APIs
jest.mock('../services/api');

const mockFaultsList = [
  {
    idno: 3759,
    issue: 'AO188 Tracking Error',
    solution: 'Reset system',
    sdescribe: 'Reset tracking',
    section: 'AO',
    status: 'Active',
    datein: '2025-12-11T10:00:00',
  },
  {
    idno: 4767,
    issue: 'Power Supply Failure',
    solution: 'Replace unit',
    sdescribe: 'Replace power supply',
    section: 'IR',
    status: 'Active',
    datein: '2025-12-10T15:30:00',
  },
];

const mockSections = ['AO', 'IR', 'CS', 'LGSF'];

describe('FATSList Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock API responses
    fatsAPI.getAll.mockResolvedValue(mockFaultsList);
    fatsAPI.searchByIdno.mockResolvedValue([mockFaultsList[0]]);
    referenceAPI.getSections.mockResolvedValue(mockSections);
  });

  test('renders FATS list table', async () => {
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText('AO188 Tracking Error')).toBeInTheDocument();
      expect(screen.getByText('Power Supply Failure')).toBeInTheDocument();
    });
  });

  test('renders table headers correctly', async () => {
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText('IDNo')).toBeInTheDocument();
      expect(screen.getByText('Date')).toBeInTheDocument();
      expect(screen.getByText('Section')).toBeInTheDocument();
      expect(screen.getByText('Issue')).toBeInTheDocument();
      expect(screen.getByText('Solution')).toBeInTheDocument();
      expect(screen.getByText('Actions')).toBeInTheDocument();
    });
  });

  test('search by ID number', async () => {
    const user = userEvent.setup();
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    // Find search input
    const searchInput = screen.getByLabelText(/search/i);
    
    // Type ID number
    await user.type(searchInput, '3759');
    
    // Click search button
    const searchButton = screen.getByRole('button', { name: /search/i });
    await user.click(searchButton);
    
    // Verify searchByIdno was called
    await waitFor(() => {
      expect(fatsAPI.searchByIdno).toHaveBeenCalledWith('3759');
    });
  });

  test('search by keywords', async () => {
    const user = userEvent.setup();
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    const searchInput = screen.getByLabelText(/search/i);
    
    // Type keywords
    await user.type(searchInput, 'tracking error');
    
    const searchButton = screen.getByRole('button', { name: /search/i });
    await user.click(searchButton);
    
    // Verify API was called
    await waitFor(() => {
      expect(fatsAPI.getAll).toHaveBeenCalled();
    });
  });

  test('search by phrase (with quotes)', async () => {
    const user = userEvent.setup();
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    const searchInput = screen.getByLabelText(/search/i);
    
    // Type phrase with quotes
    await user.type(searchInput, '"tracking error"');
    
    const searchButton = screen.getByRole('button', { name: /search/i });
    await user.click(searchButton);
    
    // Verify phrase search
    await waitFor(() => {
      expect(fatsAPI.getAll).toHaveBeenCalledWith(
        expect.objectContaining({
          search: 'tracking error',  // Quotes removed
        })
      );
    });
  });

  test('filter by section', async () => {
    const user = userEvent.setup();
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    // Wait for sections to load
    await waitFor(() => {
      expect(referenceAPI.getSections).toHaveBeenCalled();
    });
    
    // Select a section
    const sectionSelect = screen.getByLabelText(/section/i);
    await user.click(sectionSelect);
    
    // Select AO option
    const aoOption = screen.getByText('AO');
    await user.click(aoOption);
    
    // Verify filtered API call
    await waitFor(() => {
      expect(fatsAPI.getAll).toHaveBeenCalledWith(
        expect.objectContaining({
          section: 'AO',
        })
      );
    });
  });

  test('calls onViewFATS when View button clicked', async () => {
    const mockOnViewFATS = jest.fn();
    const user = userEvent.setup();
    
    render(<FATSList onViewFATS={mockOnViewFATS} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText('AO188 Tracking Error')).toBeInTheDocument();
    });
    
    // Find and click View button for first fault
    const viewButtons = screen.getAllByTitle(/View Details/i);
    await user.click(viewButtons[0]);
    
    expect(mockOnViewFATS).toHaveBeenCalledWith(3759);
  });

  test('calls onEditFATS when Edit button clicked', async () => {
    const mockOnEditFATS = jest.fn();
    const user = userEvent.setup();
    
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={mockOnEditFATS} onAddComment={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText('AO188 Tracking Error')).toBeInTheDocument();
    });
    
    // Find and click Edit button
    const editButtons = screen.getAllByTitle(/Edit/i);
    await user.click(editButtons[0]);
    
    expect(mockOnEditFATS).toHaveBeenCalledWith(3759);
  });

  test('calls onAddComment when Comment button clicked', async () => {
    const mockOnAddComment = jest.fn();
    const user = userEvent.setup();
    
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={mockOnAddComment} />);
    
    await waitFor(() => {
      expect(screen.getByText('AO188 Tracking Error')).toBeInTheDocument();
    });
    
    // Find and click Comment button
    const commentButtons = screen.getAllByTitle(/Add Comment/i);
    await user.click(commentButtons[0]);
    
    expect(mockOnAddComment).toHaveBeenCalledWith(3759);
  });

  test('shows loading state', () => {
    // Mock API to delay
    fatsAPI.getAll.mockImplementation(() => new Promise(() => {}));
    
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    // Should show loading indicator
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  test('shows error message on API failure', async () => {
    fatsAPI.getAll.mockRejectedValue(new Error('API Error'));
    
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('shows "No faults found" when no results', async () => {
    fatsAPI.getAll.mockResolvedValue([]);
    
    render(<FATSList onViewFATS={jest.fn()} onEditFATS={jest.fn()} onAddComment={jest.fn()} />);
    
    await waitFor(() => {
      expect(screen.getByText(/No faults found/i)).toBeInTheDocument();
    });
  });

  test('refresh method reloads data', async () => {
    const ref = React.createRef();
    render(
      <FATSList 
        ref={ref}
        onViewFATS={jest.fn()} 
        onEditFATS={jest.fn()} 
        onAddComment={jest.fn()} 
      />
    );
    
    await waitFor(() => {
      expect(fatsAPI.getAll).toHaveBeenCalledTimes(1);
    });
    
    // Call refresh
    ref.current.refresh();
    
    await waitFor(() => {
      expect(fatsAPI.getAll).toHaveBeenCalledTimes(2);
    });
  });
});

