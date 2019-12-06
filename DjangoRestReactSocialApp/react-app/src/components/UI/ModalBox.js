import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Modal, Button } from 'react-bootstrap'
import _ from 'underscore'

export class ModalBox extends Component {
  render () {
    const { actions, performActionItem, children, size, heading, content, modalClass, modalClassHistory } = this.props
    const Content = content
    const actionBar = _.map(actions, action => (
      <Button key={action} onClick={() => performActionItem(action)} color="primary">
        {action}
      </Button>
    ))

    return (
      <div>
        <Modal centered aria-labelledby="contained-modal-title-vcenter" className={[modalClass, modalClassHistory]} show size={size}>
          <Modal.Header>
            <Modal.Title>
              {heading}
            </Modal.Title>
            { typeof Content === 'function' ? <Content /> : Content}
          </Modal.Header>

          <Modal.Body>
            {children}
          </Modal.Body>

          <Modal.Footer>
            {actionBar}
          </Modal.Footer>
        </Modal>
      </div>
    )
  }
}

ModalBox.propTypes = {
  actions: PropTypes.any,
  children: PropTypes.any,
  content: PropTypes.any,
  heading: PropTypes.any,
  modalClass: PropTypes.any,
  modalClassHistory: PropTypes.any,
  performActionItem: PropTypes.any,
  size: PropTypes.any
}
