import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Carousel } from 'react-bootstrap';

export default class NewsSlider extends Component{

    renderNews() {
        return this.props.news.map(news => {
            return(
                
                <Carousel.Item key={news.id}>
                    <Link to={`/news/${news.id}`}>
                        <img width='100%' height='100%' alt="900x500" src={news.image_url}/>
                    </Link>
                    <Carousel.Caption>
                        <h3>{news.title}</h3>
                        <p>{news.summary}</p>
                    </Carousel.Caption>
                </Carousel.Item>
                
            ); 
        })
    }
    render(){
        if(!this.props.news) {
            <div>Loading ...</div>
        }
        return(
            <div className="news-slider">
                <Carousel wrap={true}>
                    {this.renderNews()}
                </Carousel>
            </div>
        );
    }
}