import { simpleAction } from "../actions/simpleActions";
import { compose } from "redux";
import { connect } from 'react-redux'

const mapStateToProps = state => console.log(state) || ({ result: state.simple.result })

const mapDispatchToProps = dispatch => ({
    simpleAction: () => dispatch(simpleAction())
})

export default compose(
    connect(mapStateToProps, mapDispatchToProps)
)