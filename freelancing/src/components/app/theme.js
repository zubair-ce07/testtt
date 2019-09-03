const color = {
  tint: {
    red: [
      "#f22a2a",
      "#f65858",
      "#f68181",
      "#f6c5c5",
      "#f6dfdf",

    ]
  },
  shade: {

  }
}
export default {
  main: '#3cb371',
  tint: [
    "#3cb371",
    "#4fba7f",
    "#62c28d",
    "#76c99b",
    "#8ad1a9",
    "#9dd9b8",
    "#b1e0c6",
    "#c4e8d4",
    "#d8efe2",
    "#ebf7f0"
  ],
  accent: '#70B14F',
  bg: '#f0f0f0',
  color: { ...color }
}

export const invertTheme = {
  main: '#f0f0f0',
  tint: [
    "#3cb371",
    "#4fba7f",
    "#62c28d",
    "#76c99b",
    "#8ad1a9",
    "#9dd9b8",
    "#b1e0c6",
    "#c4e8d4",
    "#d8efe2",
    "#ebf7f0"
  ],
  accent: '#ffffff',
  bg: 'mediumseagreen',
  color: { ...color }
}
