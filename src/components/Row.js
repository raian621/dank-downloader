import './Row.css'

export const Row = ({ children, className }) => {
  return (
    <tr className={className}>
      { children }
    </tr>
  )
}