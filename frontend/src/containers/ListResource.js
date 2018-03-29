
import React from 'react';
import {Link} from 'react-router-dom'
import Timestamp from 'react-timestamp';

const ListResource = (props) => (
    <div className='ui top attached tabular menu'>

        {
            props.resource.map((item) => (
                <div key={item.id} className={'row'}>
                    { props.mode==='posts' &&

                    <div className={'col-md-2'}>
                        <Link to={`${props.path}/${item.id}`}>{item.title}</Link>

                    </div>
                    }
                    {
                        props.mode==='category-posts' &&
                        <div className={'col-md-2'}>
                            {item.title}
                        </div>
                    }

                    <div className={'col-md-3'}>
                        {item.body}
                    </div>
                    <div className={'col-md-2'}>
                        {item.author}
                    </div>
                    <div className={'col-md-2'}>
                        <Timestamp time={item.timestamp}/>
                    </div>
                    <div className={'col-md-2'}>
                        {item.voteScore}
                    </div>
                    {
                        props.mode!=='category-posts' &&
                        <div className={'col-md-1'}>
                            <span className={'glyphicon glyphicon-edit'}
                                  onClick={() => props.onEditClick(item)}> </span>
                            <span className={'glyphicon glyphicon-remove'}
                                  onClick={() => props.onDeleteClick(item.id)}> </span>
                        </div>
                    }

                </div>
            ))
        }
    </div>
);

export default ListResource


