import React, { Component } from 'react';
import { Card,CardImg, CardTitle, Row, Col, Container } from 'reactstrap';

const textColor = {
    color: 'black'
};

class Cards extends Component {

    createCards() {
        let dataList = this.props.dataJson;

        const cols=dataList.map((data, index)=>{
            return(
                <Col xs="3" md="3" onClick={() => this.props.onClickHandler(data.id.videoId)} key={index}>
                    <Card body>
                        <CardTitle style={textColor}>{data.snippet.title}</CardTitle>
                        <CardImg top width="100%" src={data.snippet.thumbnails.high.url} alt="Card image cap" />
                    </Card>
                </Col>
            )
        });

        return <Row>{cols}</Row>;
    }

    
    render() {
        return (
            <Container>{this.createCards()}</Container>
        )
    }
}

export { Cards };
