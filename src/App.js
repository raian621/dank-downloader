import { MediaListContainer } from './components';
import './App.css';
import { ItemRow } from './components/ItemRow';

function App() {
  return (
    <div class="media-area">
      <section className="list-area">
        <div className='list-area-inner'>
        <h1>PLAYLISTS</h1>
        <MediaListContainer>
          <ItemRow>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
          </ItemRow>
          <ItemRow>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
          </ItemRow>
          <ItemRow>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
          </ItemRow>
          <ItemRow>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
            <p>sdffd</p>
          </ItemRow>
        </MediaListContainer>
        </div>
      </section>
      <section className="list-area">
      <div className='list-area-inner'>
      <h1>MEDIA</h1>
      <MediaListContainer>
        
        <ItemRow>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
        </ItemRow>
        <ItemRow>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
        </ItemRow>
        <ItemRow>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
        </ItemRow>
        <ItemRow>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
        </ItemRow>
        <ItemRow>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
          <p>sdffd</p>
        </ItemRow>
      </MediaListContainer>
      </div>
    </section>
    </div>
  );
}

export default App;
