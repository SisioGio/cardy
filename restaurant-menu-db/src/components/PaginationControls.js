interface PaginationProps {
  page: number;
  setPage: (page: number) => void;
  totalPages: number;
  maxVisiblePages?: number; // default 5
}

export default function PaginationControls({
  page,
  setPage,
  totalPages,
  maxVisiblePages = 5,
}: PaginationProps) {
  if (totalPages <= 1) return null;

  const getPageNumbers = () => {
    const pages = [];
    const half = Math.floor(maxVisiblePages / 2);
    let start = Math.max(page - half, 1);
    let end = start + maxVisiblePages - 1;

    if (end > totalPages) {
      end = totalPages;
      start = Math.max(end - maxVisiblePages + 1, 1);
    }

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="flex justify-center items-center gap-2 mt-4 flex-wrap">
      <button
        onClick={() => setPage(1)}
        disabled={page === 1}
        className="px-3 py-1 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        First
      </button>

      <button
        onClick={() => setPage(Math.max(page - 1, 1))}
        disabled={page === 1}
        className="px-3 py-1 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Prev
      </button>

      {pageNumbers[0] > 1 && (
        <span className="px-2 text-gray-500">...</span>
      )}

      {pageNumbers.map((p) => (
        <button
          key={p}
          onClick={() => setPage(p)}
          className={`px-3 py-1 rounded-lg border transition ${
            p === page
              ? "bg-gray-300 font-semibold text-gray-900"
              : "border-gray-300 text-gray-700 hover:bg-gray-100"
          }`}
        >
          {p}
        </button>
      ))}

      {pageNumbers[pageNumbers.length - 1] < totalPages && (
        <span className="px-2 text-gray-500">...</span>
      )}

      <button
        onClick={() => setPage(Math.min(page + 1, totalPages))}
        disabled={page === totalPages}
        className="px-3 py-1 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
      </button>

      <button
        onClick={() => setPage(totalPages)}
        disabled={page === totalPages}
        className="px-3 py-1 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Last
      </button>
    </div>
  );
}
