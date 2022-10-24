import React from "react";

export default (props) => (
  <div
    style={{
      textDecoration: props.todo.complete ? "line-through" : "",
    }}
    onClick={props.itemToggleComplete}
  >
    {props.todo.text}
  </div>
);

// function ToDo(text) {
//   return <div>{text}</div>;
// }

// export default ToDo;
