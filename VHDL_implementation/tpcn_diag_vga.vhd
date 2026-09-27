library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Minimal 640x480 VGA diagnostic view.  This module consumes only counters
-- from the diagnostic branch and has no connection to the TPCN datapath.
entity tpcn_diag_vga is
  port (
    clk_25mhz    : in  std_logic;
    viz_rst      : in  std_logic;
    active_cells : in  unsigned(7 downto 0);
    dropped_count: in  unsigned(31 downto 0);
    hsync        : out std_logic;
    vsync        : out std_logic;
    red          : out std_logic_vector(3 downto 0);
    green        : out std_logic_vector(3 downto 0);
    blue         : out std_logic_vector(3 downto 0)
  );
end entity;

architecture rtl of tpcn_diag_vga is
  signal x : integer range 0 to 799 := 0;
  signal y : integer range 0 to 524 := 0;
begin
  process(clk_25mhz)
  begin
    if rising_edge(clk_25mhz) then
      if viz_rst = '1' then
        x <= 0;
        y <= 0;
      elsif x = 799 then
        x <= 0;
        if y = 524 then
          y <= 0;
        else
          y <= y + 1;
        end if;
      else
        x <= x + 1;
      end if;
    end if;
  end process;

  hsync <= '0' when x >= 656 and x < 752 else '1';
  vsync <= '0' when y >= 490 and y < 492 else '1';

  process(x, y, active_cells, dropped_count)
    variable cell_index : integer;
  begin
    red   <= (others => '0');
    green <= (others => '0');
    blue  <= (others => '0');
    if x < 256 and y < 256 then
      cell_index := (y / 16) * 16 + (x / 16);
      if cell_index < to_integer(active_cells) then
        green <= (others => '1');
      end if;
    end if;
    if dropped_count /= 0 and x < 16 and y < 16 then
      red <= (others => '1');
    end if;
  end process;
end architecture;