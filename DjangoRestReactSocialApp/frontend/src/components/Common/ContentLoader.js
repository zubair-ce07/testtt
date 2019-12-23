// react-hooks/rules-of-hooks
import React from 'react'
import PropTypes from 'prop-types'
import LoaderSpinner from 'react-loader-spinner'
import BlockUi from 'react-block-ui'
import { useSelector } from 'react-redux'
import 'react-block-ui/style.css'
import lodash from 'lodash'

const BlockUiComponent = (props) => {
  const { children, loadingRef, loaderType, blocking } = props

  let bl = true
  bl = !!useSelector(state => lodash.get(state, loadingRef))
  if (loadingRef) {
    // bl = !!useSelector(state => lodash.get(state, loadingRef))
  } else {
    bl = blocking
  }

  const lt = loaderType || 'ThreeDots'
  return (
    <BlockUi className="loaderblock" blocking={bl} keepInView loader={<LoaderSpinner type={lt} color="#0C5BBA" />}>
      {children}
    </BlockUi>
  )
}

BlockUiComponent.propTypes = {
  blocking: PropTypes.any,
  children: PropTypes.any,
  loaderType: PropTypes.any,
  loadingRef: PropTypes.any
}

const BlockUiFieldComponent = (props) => {
  const { children, loadingRef, loaderType, blocking } = props

  let bl = true
  bl = !!useSelector(state => lodash.get(state, loadingRef))
  if (loadingRef) {
    // react-hooks/rules-of-hooks

  } else {
    bl = blocking
  }

  const lt = loaderType || 'ThreeDots'
  return (
    <BlockUi className="fieldloaderblock" blocking={bl} keepInView loader={<LoaderSpinner type={lt} color="#0C5BBA" width={30} height={30} />}>
      {children}
    </BlockUi>
  )
}

BlockUiFieldComponent.propTypes = {
  blocking: PropTypes.any,
  children: PropTypes.any,
  loaderType: PropTypes.any,
  loadingRef: PropTypes.any
}

export const Loader = (props) => {
  Loader.propTypes = {
    type: PropTypes.string.isRequired
  }
  const { type } = props

  return (
    <>
      {
        type === 'BlockUi' && <BlockUiComponent {...props}></BlockUiComponent>
      }
      {
        type === 'BlockUiField' && <BlockUiFieldComponent {...props}></BlockUiFieldComponent>
      }
    </>
  )
}
