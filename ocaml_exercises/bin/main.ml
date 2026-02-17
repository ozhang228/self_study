let rec last_two arr =
  match arr with 
  | [] | [_] -> None 
  | [x; y] -> Some (x, y)
  | _ :: tail -> last_two tail;;

assert (last_two ["a"] = None);;
assert (last_two ["a"; "b"] = Some ("a", "b"));;
assert (last_two ["a"; "b"; "c"] = Some ("b", "c"));;


