import { faPlay } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { Row } from "./Row"
import { Table } from "./Table"

export const MediaTable = () => {
  const rows = [
    {
      title: "Title",
      subTitle: "Subtitle",
      length: "1:20",
      format: "mp3",
      location: "/path/to/thing"
    },
    {
      title: "Title",
      subTitle: "Subtitle",
      length: "1:20",
      format: "mp3",
      location: "/path/to/thing"
    },
    {
      title: "Title",
      subTitle: "Subtitle",
      length: "1:20",
      format: "mp3",
      location: "/path/to/thing"
    },
  ]

  return (
    <Table>
      <Row className="row head">
        <th></th>
        <th>TITLE</th>
        <th>LENGTH</th>
        <th>FORMAT</th>
        <th>LOCATION</th>
      </Row>
      {rows.length > 0 && rows.map((row, key) => {
        return (
        <Row id={`row_${key}`} key={`row_${key}`} className="row item">
          {
              <>
                <td>
                  <FontAwesomeIcon icon={faPlay}/>
                </td>
                <td>{row.title}</td>
                <td>{row.length}</td>
                <td>{row.format}</td>
                <td>{row.location}</td>
              </>
          }
        </Row>
        )
      })}
    </Table>
  )
}