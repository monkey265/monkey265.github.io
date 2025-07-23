---
title: "HDL tips & tricks"
permalink: /hdl_tips/
author_profile: false
---

# Signal spy

Absolutely briliant way to 

`init_signal_spy( spy_object, dest_object, verbose);`

It is necessary to include modelsim lib like this, works in Questasim also.

```
library modelsim_lib;
use modelsim_lib.util.all;
```

Complete example of usage:

```
library modelsim_lib;
use modelsim_lib.util.all;
entity top is
end;

architecture ...
  signal top_sig1 : std_logic;
begin
  ...
  spy_process : process
  begin
    init_signal_spy("/top/uut/inst1/sig1","/top_sig1",1);
    wait;
  end process spy_process;
  ...
end; 
```



# References
[Signal spy](http://www.pldworld.com/_hdl/2/_ref/se_html/manual_html/c_vhdl29.html)