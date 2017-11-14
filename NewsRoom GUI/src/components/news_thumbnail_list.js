import React, { Component } from 'react';
import { Thumbnail } from 'react-bootstrap';
import { Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function trimText(text, limit){
    return text.length > limit ? text.slice(0,limit)+'...': text;
}
    
const NewsThumbnail = ({ news_list }) => {
    return (
        <div>
            {news_list.map( news => {
                return (
                    <div key={news.id} className="news-thumbnail">
                        <Col md={4} sm={6} xs={12}>
                            <Link to={`/news/${news.id}`}>
                            <Thumbnail src={ news.image_url } alt={news.title}>
                                <h3>{trimText(news.title, 37)}</h3>
                                <p className="trim-content">{trimText(news.summary, 155)}</p>
                            </Thumbnail>
                            </Link>
                        </Col>
                    </div>
                );
            })}
        </div>
    );
}
    
export default NewsThumbnail;