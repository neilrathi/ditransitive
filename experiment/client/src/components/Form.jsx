import React from "react";
import { Button } from "../components/Button";

export function Form({
  children,
  handleClick = null,
  className = ""
}) {
  return (
    <form>
      <input type = "text" /><br></br>
      <Button children={children} handleClick={handleClick} className={className} type = 'submit'/>
    </form>
  );
}