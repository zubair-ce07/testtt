import React from 'react'
// import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import { fetchSaloons } from '../actions/saloon_action'

class ListSaloon extends React.Component {
    card_style = {
        margin: '10px',
        width: '100%'
    }

    componentDidMount() {
        this.props.fetchSaloons();
    }

    render() {

        const { saloons } = this.props
        const saloonsList = saloons ? (
            saloons.map((saloon) => {
                return (
                    saloon.shop_name ? (<div className="card" style={this.card_style} key={saloon.id}>
                        <div className="card-header">
                            {saloon.shop_name}
                        </div>
                        <div className="card-body">
                            <h5 className="card-title">Phone No : {saloon.phone_no}</h5>
                            <p className="card-text">Address : {saloon.address}</p>
                            <a href="{% url 'shop_slots' saloon.shop_name %}" className="btn btn-primary">Reserve a time slot</a>
                        </div>
                    </div>) : (false)
                )
            })
        ) : (
                this.props.successStatus ? (
                    <div className="card-header">
                        No Saloon To be Listed
                            </div>
                ) : (
                        <div className="card" style={this.card_style}>
                            <div className="card-header">
                                Error getting Saloons
                            </div>
                        </div>
                    )
            )

        return (
            <div className="container">
                {saloonsList}
            </div>

        )
    }
}

const mapStateToPropos = (state) => {
    return {
        saloons: state.saloons,
        successStatus: state.successStatus
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchSaloons: () => {
            dispatch(fetchSaloons());
        }
    };
};

export default connect(mapStateToPropos, mapDispatchToProps)(ListSaloon)