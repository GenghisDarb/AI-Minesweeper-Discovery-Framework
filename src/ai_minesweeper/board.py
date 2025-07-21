"""
Minesweeper Board implementation with χ-recursive form and TORUS theory alignment.

This module provides the core Board class with:
- Dynamic mine count tracking for risk tuning
- Safe-flag handling
- Neighbor references consistent with χ-recursive model
- Integrated logging for TORUS theory alignment
"""

import logging
from typing import List, Tuple, Set, Dict, Optional
from enum import Enum


class CellState(Enum):
    """Cell states in the minesweeper board."""
    HIDDEN = "hidden"
    REVEALED = "revealed" 
    FLAGGED = "flagged"
    SAFE_FLAGGED = "safe_flagged"  # χ-recursive safe flag


class Board:
    """
    Minesweeper board with χ-recursive form and TORUS theory integration.
    
    Features:
    - Dynamic risk tuning through mine count tracking
    - Safe-flag handling for χ-recursive decision making
    - Neighbor references consistent with TORUS topology
    - Integrated logging for confidence assessment
    """
    
    def __init__(self, width: int, height: int, mine_count: int):
        """
        Initialize the minesweeper board.
        
        Args:
            width: Board width
            height: Board height  
            mine_count: Number of mines to place
        """
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.remaining_mines = mine_count
        
        # Initialize board state
        self.mines: Set[Tuple[int, int]] = set()
        self.cell_states: Dict[Tuple[int, int], CellState] = {}
        self.revealed_numbers: Dict[Tuple[int, int], int] = {}
        
        # Initialize all cells as hidden
        for x in range(width):
            for y in range(height):
                self.cell_states[(x, y)] = CellState.HIDDEN
                
        # χ-recursive tracking
        self.safe_flags: Set[Tuple[int, int]] = set()
        self.confidence_history: List[float] = []
        
        # TORUS theory integration
        self.chi_cycle_count = 0
        self.recursive_depth = 0
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Board initialized: {width}x{height} with {mine_count} mines")
    
    def place_mines(self, first_click: Tuple[int, int]) -> None:
        """
        Place mines on the board, avoiding the first click position.
        
        Args:
            first_click: Coordinates of first click to avoid
        """
        import random
        
        available_positions = []
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) != first_click:
                    available_positions.append((x, y))
        
        self.mines = set(random.sample(available_positions, self.mine_count))
        self.logger.info(f"Mines placed: {len(self.mines)} mines positioned")
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get neighbor coordinates for a cell with TORUS topology support.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            List of neighbor coordinates
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        
        return neighbors
    
    def get_mine_count_around(self, x: int, y: int) -> int:
        """
        Get the number of mines around a cell.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            Number of mines in neighboring cells
        """
        count = 0
        for nx, ny in self.get_neighbors(x, y):
            if (nx, ny) in self.mines:
                count += 1
        return count
    
    def reveal_cell(self, x: int, y: int) -> bool:
        """
        Reveal a cell and handle cascading reveals.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            True if game continues, False if mine hit
        """
        if (x, y) in self.mines:
            self.logger.warning(f"Mine hit at ({x}, {y})")
            return False
            
        if self.cell_states[(x, y)] != CellState.HIDDEN:
            return True
            
        self.cell_states[(x, y)] = CellState.REVEALED
        mine_count = self.get_mine_count_around(x, y)
        self.revealed_numbers[(x, y)] = mine_count
        
        # Cascade if no mines around (χ-recursive expansion)
        if mine_count == 0:
            self.recursive_depth += 1
            for nx, ny in self.get_neighbors(x, y):
                if self.cell_states[(nx, ny)] == CellState.HIDDEN:
                    self.reveal_cell(nx, ny)
            self.recursive_depth -= 1
            
        self.logger.debug(f"Cell ({x}, {y}) revealed with {mine_count} neighboring mines")
        return True
    
    def flag_cell(self, x: int, y: int, safe_flag: bool = False) -> None:
        """
        Flag a cell as containing a mine.
        
        Args:
            x, y: Cell coordinates
            safe_flag: Whether this is a χ-recursive safe flag
        """
        if self.cell_states[(x, y)] == CellState.HIDDEN:
            if safe_flag:
                self.cell_states[(x, y)] = CellState.SAFE_FLAGGED
                self.safe_flags.add((x, y))
                self.logger.debug(f"Safe flag placed at ({x}, {y})")
            else:
                self.cell_states[(x, y)] = CellState.FLAGGED
                self.remaining_mines -= 1
                self.logger.debug(f"Mine flag placed at ({x}, {y})")
    
    def unflag_cell(self, x: int, y: int) -> None:
        """
        Remove flag from a cell.
        
        Args:
            x, y: Cell coordinates
        """
        if self.cell_states[(x, y)] == CellState.FLAGGED:
            self.cell_states[(x, y)] = CellState.HIDDEN
            self.remaining_mines += 1
        elif self.cell_states[(x, y)] == CellState.SAFE_FLAGGED:
            self.cell_states[(x, y)] = CellState.HIDDEN
            self.safe_flags.discard((x, y))
        
        self.logger.debug(f"Flag removed from ({x}, {y})")
    
    def get_hidden_cells(self) -> Set[Tuple[int, int]]:
        """Get all hidden cells."""
        return {pos for pos, state in self.cell_states.items() 
                if state == CellState.HIDDEN}
    
    def get_flagged_cells(self) -> Set[Tuple[int, int]]:
        """Get all flagged cells (including safe flags)."""
        return {pos for pos, state in self.cell_states.items() 
                if state in [CellState.FLAGGED, CellState.SAFE_FLAGGED]}
    
    def get_revealed_cells(self) -> Set[Tuple[int, int]]:
        """Get all revealed cells."""
        return {pos for pos, state in self.cell_states.items() 
                if state == CellState.REVEALED}
    
    def is_solved(self) -> bool:
        """Check if the board is solved."""
        hidden_cells = self.get_hidden_cells()
        flagged_cells = self.get_flagged_cells()
        
        # All mines should be flagged and no other cells hidden
        return len(hidden_cells) == 0 and len(flagged_cells) == self.mine_count
    
    def update_chi_cycle(self, confidence: float) -> None:
        """
        Update χ-cycle tracking for TORUS theory integration.
        
        Args:
            confidence: Current solver confidence level
        """
        self.confidence_history.append(confidence)
        self.chi_cycle_count += 1
        
        # χ-recursive feedback mechanism
        if len(self.confidence_history) > 10:
            recent_trend = sum(self.confidence_history[-5:]) / 5
            if recent_trend > 0.8:
                # High confidence - χ-cycle positive feedback
                self.logger.info(f"χ-cycle positive feedback at count {self.chi_cycle_count}")
            elif recent_trend < 0.3:
                # Low confidence - χ-cycle negative feedback
                self.logger.warning(f"χ-cycle negative feedback at count {self.chi_cycle_count}")
    
    def get_state_summary(self) -> Dict:
        """Get a summary of the current board state."""
        return {
            "width": self.width,
            "height": self.height,
            "mine_count": self.mine_count,
            "remaining_mines": self.remaining_mines,
            "hidden_cells": len(self.get_hidden_cells()),
            "revealed_cells": len(self.get_revealed_cells()),
            "flagged_cells": len(self.get_flagged_cells()),
            "safe_flags": len(self.safe_flags),
            "chi_cycle_count": self.chi_cycle_count,
            "recursive_depth": self.recursive_depth,
            "is_solved": self.is_solved()
        }