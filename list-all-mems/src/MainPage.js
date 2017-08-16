import React from 'react';
import MemDiv from './MemDiv';

class MainPage extends React.Component{

    render(){

        let mems = this.props.mems.map(mem => {
             return <MemDiv mem={mem} key={mem.id}/>
        });
        console.log(mems);
        return (
            <div >
                {mems}
            </div>
        );
    }
}
export default MainPage;
