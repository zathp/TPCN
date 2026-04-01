library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_tpcn_cell is
end entity;

architecture sim of tb_tpcn_cell is
  constant PATHWAYS   : positive := 10;
  constant DATA_WIDTH : positive := 16;

  signal clk             : std_logic := '0';
  signal rst             : std_logic := '1';
  signal en              : std_logic := '0';
  signal h_in            : signed(DATA_WIDTH - 1 downto 0) := (others => '0');
  signal pathway_vals    : signed(PATHWAYS * DATA_WIDTH - 1 downto 0) := (others => '0');
  signal pathway_gates   : unsigned(PATHWAYS * DATA_WIDTH - 1 downto 0) := (others => '0');
  signal err_in          : signed(DATA_WIDTH - 1 downto 0) := (others => '0');
  signal use_delayed_err : std_logic := '0';
  signal leak_alpha      : unsigned(DATA_WIDTH - 1 downto 0) := to_unsigned(128, DATA_WIDTH); -- 0.5
  signal err_gain        : unsigned(DATA_WIDTH - 1 downto 0) := to_unsigned(32, DATA_WIDTH);  -- 0.125
  signal h_out           : signed(DATA_WIDTH - 1 downto 0);
  signal err_out         : signed(DATA_WIDTH - 1 downto 0);

  constant CLK_PERIOD : time := 10 ns;

  procedure set_pathway(
    signal vals  : inout signed(PATHWAYS * DATA_WIDTH - 1 downto 0);
    signal gates : inout unsigned(PATHWAYS * DATA_WIDTH - 1 downto 0);
    idx          : in integer;
    val_q88      : in integer;
    gate_q88     : in integer
  ) is
    variable lo : integer;
    variable hi : integer;
  begin
    lo := idx * DATA_WIDTH;
    hi := (idx + 1) * DATA_WIDTH - 1;
    vals(hi downto lo)  <= to_signed(val_q88, DATA_WIDTH);
    gates(hi downto lo) <= to_unsigned(gate_q88, DATA_WIDTH);
  end procedure;

begin
  clk <= not clk after CLK_PERIOD / 2;

  dut: entity work.tpcn_cell
    generic map (
      PATHWAYS       => PATHWAYS,
      DATA_WIDTH     => DATA_WIDTH,
      ERROR_BUF_SIZE => 8
    )
    port map (
      clk             => clk,
      rst             => rst,
      en              => en,
      h_in            => h_in,
      pathway_vals    => pathway_vals,
      pathway_gates   => pathway_gates,
      err_in          => err_in,
      use_delayed_err => use_delayed_err,
      leak_alpha      => leak_alpha,
      err_gain        => err_gain,
      h_out           => h_out,
      err_out         => err_out
    );

  stim: process
  begin
    -- Reset
    wait for 5 * CLK_PERIOD;
    rst <= '0';
    en  <= '1';

    -- Build pathway mix: two active pathways
    set_pathway(pathway_vals, pathway_gates, 0,  128, 256); -- +0.5 * 1.0
    set_pathway(pathway_vals, pathway_gates, 1, -64, 128);  -- -0.25 * 0.5

    -- Immediate error mode
    use_delayed_err <= '0';
    err_in <= to_signed(16, DATA_WIDTH); -- small positive error
    wait for 20 * CLK_PERIOD;

    -- Delayed error mode, change sign
    use_delayed_err <= '1';
    err_in <= to_signed(-24, DATA_WIDTH);
    wait for 20 * CLK_PERIOD;

    -- Increase error gain and observe stronger correction
    err_gain <= to_unsigned(64, DATA_WIDTH); -- 0.25
    wait for 20 * CLK_PERIOD;

    report "TB completed" severity note;
    wait;
  end process;

  checker: process(clk)
  begin
    if rising_edge(clk) then
      if rst = '0' and en = '1' then
        assert h_out'length = DATA_WIDTH
          report "Unexpected h_out width"
          severity error;
      end if;
    end if;
  end process;
end architecture;
