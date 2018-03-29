
import React from 'react';

const ListHeader = (props) => (
    <div className='ui top attached tabular menu'>
        <div className={'row'}>
            {   props.mode!=='comments' &&
                <div className={'col-md-2'}>
                    <b>Title</b>
                </div>
            }
            <div className={'col-md-3'}>
                <b>Detail</b>
            </div>
            <div className={'col-md-2'}>
                <b>Author</b>
            </div>

            <div className={'col-md-2'}>
                <b>Time </b>
            </div>
            <div className={'col-md-2'}>
                <b>Vote Score </b>
            </div>
            { props.mode!=='category-posts' &&

            <div className={'col-md-1'}>
                <b>Action</b>
            </div>
            }
        </div>
    </div>
);

export default ListHeader


