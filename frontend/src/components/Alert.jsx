export const Alert = ({ type = 'error', message }) => {
  if (!message) return null
  return <div className={`alert ${type}`}>{message}</div>
}
