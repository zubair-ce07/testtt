import React from 'react'
import {Grid, Row, Col} from 'react-bootstrap/lib'

const GridInstance = () => {
    const dummySentences = ['Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 'Donec hendrerit tempor tellus.', 'Donec pretium posuere tellus.', 'Proin quam nisl, tincidunt et, mattis eget, convallis nec, purus.', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.', 'Nulla posuere.', 'Donec vitae dolor.', 'Nullam tristique diam non turpis.', 'Cras placerat accumsan nulla.', 'Nullam rutrum.', 'Nam vestibulum accumsan nisl.']
    return(
        <div >
            <Grid>
                <Row className="show-grid">
                <Col sm={6} md={6}>{dummySentences.slice(0, 7).join(' ')}</Col>
                <Col sm={6} md={6}>{dummySentences.slice(0, 7).join(' ')}</Col>
                </Row>
            </Grid>
        </div>
    )
}

export default GridInstance
