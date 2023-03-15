import './Table.css'

export const Table = ({ children }) => {
  return (
    <table className="media-list-container">
      { children }
    </table>
  )
}