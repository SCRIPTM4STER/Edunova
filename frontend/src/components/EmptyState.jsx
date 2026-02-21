export const EmptyState = ({ title, subtitle }) => (
  <div className="empty-state">
    <p>
      <strong>{title}</strong>
    </p>
    {subtitle ? <p className="muted">{subtitle}</p> : null}
  </div>
)
