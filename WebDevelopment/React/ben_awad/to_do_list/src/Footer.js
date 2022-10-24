import React from "react";

function Footer({ items, setShow }) {
  return <div>
  <div>Todos left: {items.filter((item) => !item.complete).length}</div>;
  <button onClick={() => setShow('all')}>all</button>
  <button onClick={() => setShow('active')}>active</button>
  <button onClick={() => setShow('complete')}>complete</button>

  </div>
}

export default Footer;
