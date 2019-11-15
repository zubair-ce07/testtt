import React, { Component } from "react";
import IconItem from "./iconItem";
import { getRandomInt, shuffleArray } from "../util";
import { mainStyle, float, mediumSize, result } from "./styles";
import DynamicImage from "./dynamicImage";

const min = 1;
const max = 250;
const magicNumber = 9;

class IconItems extends Component {
  constructor(props) {
    super(props);
    const randomNo = getRandomInt(min, max);
    this.state = {
      toBeGuessed: randomNo,
      showResult: false,
      iconItems: []
    };
  }

  componentDidMount() {
    let iconItems = [];
    for (let i = 1; i <= 105; i++) {
      let item = { label: i };
      if (i % magicNumber === 0) {
        item["iconNameSuffix"] = this.state.toBeGuessed;
      } else {
        item["iconNameSuffix"] = getRandomInt(min, max);
      }
      iconItems.push(item);
    }
    this.setState({ iconItems });
  }

  handleShowResult = () => {
    this.setState({ showResult: true });
  };

  renderResult = () => {
    const { toBeGuessed } = this.state;
    const iconName = `icon-${toBeGuessed}.png`;

    return (
      <div
        style={result}
        className="d-flex flex-column bg-info align-items-center"
      >
        <h3 className="text-center">Here is the image ..........</h3>
        <DynamicImage style={mediumSize} name={iconName} />
      </div>
    );
  };

  render() {
    const { iconItems, showResult } = this.state;

    // shuffleArray(iconItems);
    return (
      <div
        style={mainStyle}
        className="d-flex flex-wrap align-content-center m-20 p-10"
      >
        {showResult ? (
          this.renderResult()
        ) : (
          <React.Fragment>
            <button
              style={float}
              className="btn btn-success"
              onClick={this.handleShowResult}
            >
              Read Mind's Image
            </button>
            {iconItems.map(iconItem => (
              <IconItem key={iconItem.label} iconItem={iconItem} />
            ))}
          </React.Fragment>
        )}
      </div>
    );
  }
}

export default IconItems;
