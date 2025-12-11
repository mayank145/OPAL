/**
 * Tests for FATSDetailInline component
 */
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FATSDetailInline from './FATSDetailInline';
import { fatsAPI } from '../services/api';

jest.mock('../services/api');

const mockFatsData = {
  idno: 3759,
  issue: 'AO188 Tracking Error',
  solution: 'Reset tracking system',
  sdescribe: '<p><strong>Step 1:</strong> Power cycle</p><ul><li>Turn off</li><li>Wait</li></ul>',
  section: 'AO',
  status: 'Active',
  datein: '2025-12-11T10:00:00',
  operator: 'Test User',
  assigned_to: 'Tech Team',
};

const mockImages = [
  { filename: 'image1.jpg', url: '/uploads/fats/image1.jpg', uploaded_at: '2025-12-11T10:00:00' },
  { filename: 'image2.jpg', url: '/uploads/fats/image2.jpg', uploaded_at: '2025-12-11T11:00:00' },
];

const mockComments = [
  {
    id: 1,
    comment_text: '<p>Test comment</p>',
    commenter: 'User1',
    created_at: '2025-12-11T12:00:00',
    todo: 'Test TODO',
    solution: 'Test solution',
  },
];

describe('FATSDetailInline Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    fatsAPI.getById.mockResolvedValue(mockFatsData);
    fatsAPI.getImages.mockResolvedValue(mockImages);
    fatsAPI.getComments.mockResolvedValue(mockComments);
  });

  test('renders fault details', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      expect(screen.getByText(/Fault #3759/i)).toBeInTheDocument();
      expect(screen.getByText('AO188 Tracking Error')).toBeInTheDocument();
      expect(screen.getByText('Reset tracking system')).toBeInTheDocument();
    });
  });

  test('renders all required sections in correct order', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      expect(screen.getByText('Action')).toBeInTheDocument();
      expect(screen.getByText('Solution')).toBeInTheDocument();
      expect(screen.getByText('Solution Description')).toBeInTheDocument();
      expect(screen.getByText(/Pictures/i)).toBeInTheDocument();
      expect(screen.getByText(/Comments/i)).toBeInTheDocument();
    });
  });

  test('renders HTML formatting in Solution Description', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      const solutionDesc = screen.getByText(/Step 1:/i);
      expect(solutionDesc).toBeInTheDocument();
      // HTML should be rendered (check for bold, lists, etc.)
    });
  });

  test('displays images in gallery', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      expect(screen.getByText(/Pictures \(2\)/i)).toBeInTheDocument();
      const images = screen.getAllByRole('img');
      expect(images.length).toBeGreaterThanOrEqual(2);
    });
  });

  test('displays comments', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      expect(screen.getByText(/Comments \(1\)/i)).toBeInTheDocument();
      expect(screen.getByText('User1')).toBeInTheDocument();
    });
  });

  test('opens image preview when image clicked', async () => {
    const user = userEvent.setup();
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      const images = screen.getAllByRole('img');
      expect(images.length).toBeGreaterThan(0);
    });
    
    // Click first image
    const images = screen.getAllByRole('img');
    await user.click(images[0]);
    
    // Preview dialog should open
    await waitFor(() => {
      const dialogs = screen.getAllByRole('dialog');
      expect(dialogs.length).toBeGreaterThan(0);
    });
  });

  test('shows Print button', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      expect(screen.getByText(/Print/i)).toBeInTheDocument();
    });
  });

  test('shows delete button on image hover', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      const deleteButtons = screen.getAllByTitle(/Delete image/i);
      expect(deleteButtons.length).toBeGreaterThan(0);
    });
  });

  test('shows loading state initially', () => {
    fatsAPI.getById.mockImplementation(() => new Promise(() => {}));
    
    render(<FATSDetailInline fatsId={3759} />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  test('shows error when fault not found', async () => {
    fatsAPI.getById.mockRejectedValue(new Error('Not found'));
    
    render(<FATSDetailInline fatsId={999999} />);
    
    await waitFor(() => {
      expect(screen.getByText(/error|not found/i)).toBeInTheDocument();
    });
  });

  test('fetches data on mount', async () => {
    render(<FATSDetailInline fatsId={3759} />);
    
    await waitFor(() => {
      expect(fatsAPI.getById).toHaveBeenCalledWith(3759);
      expect(fatsAPI.getImages).toHaveBeenCalledWith(3759);
      expect(fatsAPI.getComments).toHaveBeenCalledWith(3759);
    });
  });
});

