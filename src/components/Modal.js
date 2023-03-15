import './Modal.css'

export const Modal = ({ children, toggleModal }) => {

  return (
    <>
      <div className="modal-background" onClick={toggleModal}/>
      <div className="modal">
        { children }
      </div>
    </>
  )
}