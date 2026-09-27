library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Downstream-only diagnostic FIFO.  There is intentionally no ready input
-- toward the TPCN producer: a full FIFO drops a diagnostic word.
entity tpcn_diag_stream is
  generic (
    DATA_WIDTH : positive := 32;
    FIFO_DEPTH : positive := 16
  );
  port (
    clk          : in  std_logic;
    viz_rst      : in  std_logic;
    in_valid     : in  std_logic;
    in_data      : in  std_logic_vector(DATA_WIDTH - 1 downto 0);
    out_ready    : in  std_logic;
    out_valid    : out std_logic;
    out_data     : out std_logic_vector(DATA_WIDTH - 1 downto 0);
    overflow     : out std_logic;
    dropped_count: out unsigned(31 downto 0)
  );
end entity;

architecture rtl of tpcn_diag_stream is
  type fifo_t is array (0 to FIFO_DEPTH - 1) of std_logic_vector(DATA_WIDTH - 1 downto 0);
  signal fifo       : fifo_t := (others => (others => '0'));
  signal read_ptr   : integer range 0 to FIFO_DEPTH - 1 := 0;
  signal write_ptr  : integer range 0 to FIFO_DEPTH - 1 := 0;
  signal item_count : integer range 0 to FIFO_DEPTH := 0;
  signal overflow_r : std_logic := '0';
  signal dropped_r  : unsigned(31 downto 0) := (others => '0');
begin
  process(clk)
    variable next_read  : integer range 0 to FIFO_DEPTH - 1;
    variable next_write : integer range 0 to FIFO_DEPTH - 1;
    variable next_count : integer range 0 to FIFO_DEPTH;
  begin
    if rising_edge(clk) then
      if viz_rst = '1' then
        read_ptr    <= 0;
        write_ptr   <= 0;
        item_count  <= 0;
        overflow_r  <= '0';
        dropped_r   <= (others => '0');
      else
        next_read  := read_ptr;
        next_write := write_ptr;
        next_count := item_count;

        if out_ready = '1' and next_count > 0 then
          if next_read = FIFO_DEPTH - 1 then
            next_read := 0;
          else
            next_read := next_read + 1;
          end if;
          next_count := next_count - 1;
        end if;

        if in_valid = '1' then
          if next_count < FIFO_DEPTH then
            fifo(next_write) <= in_data;
            if next_write = FIFO_DEPTH - 1 then
              next_write := 0;
            else
              next_write := next_write + 1;
            end if;
            next_count := next_count + 1;
          else
            overflow_r <= '1';
            if dropped_r /= x"FFFFFFFF" then
              dropped_r <= dropped_r + 1;
            end if;
          end if;
        end if;

        read_ptr   <= next_read;
        write_ptr  <= next_write;
        item_count <= next_count;
      end if;
    end if;
  end process;

  out_valid     <= '1' when item_count > 0 else '0';
  out_data      <= fifo(read_ptr);
  overflow      <= overflow_r;
  dropped_count <= dropped_r;
end architecture;