library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_tpcn_diag_stream is
end entity;

architecture sim of tb_tpcn_diag_stream is
  signal clk           : std_logic := '0';
  signal viz_rst       : std_logic := '1';
  signal in_valid      : std_logic := '0';
  signal in_data       : std_logic_vector(31 downto 0) := (others => '0');
  signal out_ready     : std_logic := '0';
  signal out_valid     : std_logic;
  signal out_data      : std_logic_vector(31 downto 0);
  signal overflow      : std_logic;
  signal dropped_count : unsigned(31 downto 0);
begin
  clk <= not clk after 5 ns;

  dut: entity work.tpcn_diag_stream
    generic map (DATA_WIDTH => 32, FIFO_DEPTH => 2)
    port map (
      clk           => clk,
      viz_rst       => viz_rst,
      in_valid      => in_valid,
      in_data       => in_data,
      out_ready     => out_ready,
      out_valid     => out_valid,
      out_data      => out_data,
      overflow      => overflow,
      dropped_count  => dropped_count
    );

  stim: process
  begin
    wait for 15 ns;
    viz_rst <= '0';

    in_valid <= '1';
    in_data  <= x"54524331";
    wait for 10 ns;
    in_data  <= x"00010002";
    wait for 10 ns;
    in_data  <= x"DEADBEEF";
    wait for 10 ns;
    in_valid <= '0';

    assert overflow = '1'
      report "full diagnostic FIFO did not report overflow"
      severity error;
    assert dropped_count = 1
      report "diagnostic FIFO drop counter mismatch"
      severity error;

    out_ready <= '1';
    wait for 10 ns;
    assert out_data = x"00010002"
      report "diagnostic FIFO ordering mismatch"
      severity error;
    report "diagnostic stream test completed" severity note;
    wait;
  end process;
end architecture;