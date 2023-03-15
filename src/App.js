import { useState } from 'react';
import './App.css';
import downloadIcon from './assets/download64x64.png'
import { MediaTable, PlaylistTable } from './components';
import { MediaDownloadForm } from './components/forms/MediaDownloadForm';
import { Modal } from './components/Modal';
import { PlayBar } from './components/PlayBar';

function App() {
  const [showPlaylistModal, setShowPlaylistModal] = useState(false);
  const [showMediaModal, setShowMediaModal] = useState(false);
  const [playlistItems, setPlaylistItems] = useState([]);
  const [mediaItems, setMediaItems] = useState([]);

  const togglePlaylistModal = () => setShowPlaylistModal(!showPlaylistModal);
  const toggleMediaModal = () => setShowMediaModal(!showMediaModal);

  return (
    <div className="media-area">
      <section className="list-area">
        <div className='list-area-inner'>
          <div className="list-area-heading">
            <h1>PLAYLISTS</h1>
            <button onClick={togglePlaylistModal}>
              <img src={downloadIcon}></img>
            </button>
          </div>
          <div className="table-wrapper">
            <PlaylistTable playlistItems={playlistItems}/>
          </div>
        </div>
        </section>
      <section className="list-area">
        <div className='list-area-inner'>
          <div className="list-area-heading">
            <h1>MEDIA</h1>
            <button onClick={toggleMediaModal}>
              <img src={downloadIcon}></img>
            </button>
          </div>
          <div className="table-wrapper">
            <MediaTable mediaItems={mediaItems}/>
          </div>
        </div>
      </section>
      <PlayBar/>
      {showPlaylistModal && <p>adfasdfasd</p>}
      {showMediaModal && 
        <Modal toggleModal={toggleMediaModal}>
          <MediaDownloadForm/>
        </Modal>
      }
    </div>
  );
}

export default App;
