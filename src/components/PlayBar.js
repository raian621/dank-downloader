import { faBackwardStep, faForwardStep, faPause, faPlay, faRefresh, faShuffle } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { useState } from "react"

import './PlayBar.css'

export const PlayBar = () => {
  const [playState, setPlayState] = useState("pause");

  return (
    <div className="play-bar">
      <FontAwesomeIcon icon={faShuffle}/>
      <FontAwesomeIcon icon={faBackwardStep}/>
      {playState === "pause" && 
        <FontAwesomeIcon 
          icon={faPlay}
          onClick={()=>setPlayState("play")}
        />
      }
      {playState === "play" && 
        <FontAwesomeIcon
          icon={faPause}
          onClick={()=>setPlayState("pause")}
        />
      }
      <FontAwesomeIcon icon={faForwardStep}/>
      <FontAwesomeIcon icon={faRefresh}/>
    </div>
  )
}