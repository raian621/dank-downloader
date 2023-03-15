import { useState } from 'react'
import './Forms.css'

export const MediaDownloadForm = ({ setMediaItems }) => {
  const [availableResolutions, setAvailableResolutions] = useState(["no preference"]);
  const [availableFormats, setAvailableFormats] = useState(["no preference"]);
  const [fileType, setFileType] = useState("video");
  const [fileFormat, setFileFormat] = useState("no preference")

  return (
    <>
      <form>
        <fieldset>
          <label htmlFor="title">TITLE</label>
          <input name="title"/>
        </fieldset>
        <fieldset>
          <label htmlFor="subtitle">SUBTITLE</label>
          <input name="subtitle"/>
        </fieldset>
        <fieldset>
          <label htmlFor="url">URL</label>
          <input name="url"/>
        </fieldset>
        <fieldset>
          <label htmlFor="type">TYPE</label>
          <select name="type" value={fileType} onChange={(e)=>{setFileType(e.target.value)}}>
            <option name="video">video</option>
            <option name="audio">audio</option>
          </select>
        </fieldset>
        <fieldset>
          <label htmlFor="format">FORMAT</label>
          <select name="format" value={fileFormat} onChange={e=>setFileFormat(e.target.value)}>
            {availableFormats.map(item => {
              return <option key={item} value="item">{item}</option>
            })}
          </select>
        </fieldset>

        {fileType === "audio" && <fieldset>
          <label htmlFor="quality">QUALITY</label>
          <input name="quality"/>
        </fieldset>}
        {fileType === "video" && <fieldset>
          <label htmlFor="resolution">RESOLUTION</label>
          <input name="resolution"/>
        </fieldset>}
        <input type="submit"/>
      </form>
    </>
  )
}