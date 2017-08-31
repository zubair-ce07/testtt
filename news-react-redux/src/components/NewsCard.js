import React from "react";
import {Media} from "react-bootstrap";
import {Link} from "react-router-dom";

const NewsCard = (props) => {
    const news = props.news;
    return (
        <div className="news-card">
            <Media>
                <Media.Left>
                    <img src={news.image_url} alt="News"/>
                </Media.Left>
                <Media.Body>
                    <Media.Heading>
                        <Link to={/news/ + news.id}>
                            {news.title}
                        </Link>
                    </Media.Heading>
                    <p dangerouslySetInnerHTML={{__html: news.content.slice(0, 350) + '...'}}/>
                    <p>{news.pub_date}</p>
                </Media.Body>
            </Media>
            <div>
                <hr/>
            </div>
        </div>
    );

};

export default NewsCard;
