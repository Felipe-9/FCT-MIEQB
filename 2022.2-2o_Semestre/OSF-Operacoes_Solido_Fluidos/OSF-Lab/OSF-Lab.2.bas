= LAMBDA(experiment,
  LAMBDA(h1,h0,t1,t0,
    (h1-h0)/(t1-t0)
  )(
    myCells(ROW(R)-1,3+2*(experiment-1)),
    myCells(ROW(R)+0,3+2*(experiment-1)),
    myCells(ROW(R)-1,4+2*(experiment-1)),
    myCells(ROW(R)+0,4+2*(experiment-1))
  )
)(R8C)


