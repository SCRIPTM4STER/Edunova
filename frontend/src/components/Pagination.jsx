export const Pagination = ({ page, canPrev, canNext, onPrev, onNext, total }) => (
  <div className="pagination">
    <button disabled={!canPrev} onClick={onPrev}>
      Previous
    </button>
    <span>
      Page {page} {total ? `• ${total} total` : ''}
    </span>
    <button disabled={!canNext} onClick={onNext}>
      Next
    </button>
  </div>
)
