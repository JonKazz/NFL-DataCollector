"""Tests for games page scrapers."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from games_page.main import extract_player_urls_from_game_page, ETL_game_page
from games_page.ingest import GamePageScraper
from games_page.transform import GamePageTransformer


class TestGamePageScraper:
    """Test the GamePageScraper class."""
    
    def test_extract_player_urls_from_game_page(self):
        """Test extracting player URLs from a game page."""
        # Mock the scraper
        with patch('games_page.main.GamePageScraper') as mock_scraper_class:
            mock_scraper = Mock()
            mock_scraper.extract_player_ids_from_game_page.return_value = [
                'A/AdamsDa01', 'B/BradyTo00', 'C/ChaseJa00'
            ]
            mock_scraper_class.return_value = mock_scraper
            
            # Test the function
            result = extract_player_urls_from_game_page('https://example.com/game')
            
            # Verify results
            expected_urls = [
                'https://www.pro-football-reference.com/players/A/AdamsDa01.htm',
                'https://www.pro-football-reference.com/players/B/BradyTo00.htm',
                'https://www.pro-football-reference.com/players/C/ChaseJa00.htm'
            ]
            assert result == expected_urls
            
            # Verify scraper was called correctly
            mock_scraper_class.assert_called_once()
            mock_scraper.load_page.assert_called_once_with('https://example.com/game')
            mock_scraper.extract_player_ids_from_game_page.assert_called_once()
    
    def test_ETL_game_page(self):
        """Test the ETL_game_page function."""
        # Mock dependencies
        mock_loader = Mock()
        mock_scraper = Mock()
        mock_transformer = Mock()
        
        # Mock data
        mock_game_info = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        mock_team_stats = pd.DataFrame({'col1': [3, 4], 'col2': ['c', 'd']})
        mock_player_stats = pd.DataFrame({'col1': [5, 6], 'col2': ['e', 'f']})
        
        # Mock transformed data
        mock_transformed_game_info = pd.DataFrame({'transformed': [1, 2]})
        mock_transformed_team_stats = pd.DataFrame({'transformed': [3, 4]})
        mock_transformed_player_stats = pd.DataFrame({'transformed': [5, 6]})
        
        with patch('games_page.main.GamePageScraper', return_value=mock_scraper), \
             patch('games_page.main.GamePageTransformer', return_value=mock_transformer):
            
            # Setup mocks
            mock_scraper.get_game_info.return_value = mock_game_info
            mock_scraper.get_game_stats.return_value = mock_team_stats
            mock_scraper.get_game_player_stats.return_value = mock_player_stats
            
            mock_transformer.transform_game_info_df.return_value = mock_transformed_game_info
            mock_transformer.transform_game_stats_df.return_value = mock_transformed_team_stats
            mock_transformer.transform_player_stats_df.return_value = mock_transformed_player_stats
            
            # Test the function
            ETL_game_page('https://example.com/game', mock_loader)
            
            # Verify scraper was called correctly
            mock_scraper.get_game_info.assert_called_once()
            mock_scraper.get_game_stats.assert_called_once()
            mock_scraper.get_game_player_stats.assert_called_once()
            
            # Verify transformer was called correctly
            mock_transformer.assert_called_once_with(mock_game_info, mock_team_stats, mock_player_stats)
            mock_transformer.transform_game_info_df.assert_called_once()
            mock_transformer.transform_game_stats_df.assert_called_once()
            mock_transformer.transform_player_stats_df.assert_called_once()
            
            # Verify loader was called correctly
            mock_loader.insert_game_info_df.assert_called_once_with(mock_transformed_game_info)
            mock_loader.insert_game_stats_df.assert_called_once_with(mock_transformed_team_stats)
            mock_loader.insert_game_player_stats_df.assert_called_once_with(mock_transformed_player_stats)


class TestGamePageTransformer:
    """Test the GamePageTransformer class."""
    
    def test_transform_game_info_df(self):
        """Test transforming game info dataframe."""
        # Create test data
        game_info = pd.DataFrame({
            'date': ['2024-01-01'],
            'home_team': ['KAN'],
            'away_team': ['BUF']
        })
        team_stats = pd.DataFrame({'col1': [1]})
        player_stats = pd.DataFrame({'col1': [1]})
        
        transformer = GamePageTransformer(game_info, team_stats, player_stats)
        
        # Test the transform method
        result = transformer.transform_game_info_df()
        
        # Verify result is a dataframe
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_transform_game_stats_df(self):
        """Test transforming game stats dataframe."""
        # Create test data
        game_info = pd.DataFrame({'col1': [1]})
        team_stats = pd.DataFrame({
            'team': ['KAN', 'BUF'],
            'points': [24, 20]
        })
        player_stats = pd.DataFrame({'col1': [1]})
        
        transformer = GamePageTransformer(game_info, team_stats, player_stats)
        
        # Test the transform method
        result = transformer.transform_game_stats_df()
        
        # Verify result is a dataframe
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_transform_player_stats_df(self):
        """Test transforming player stats dataframe."""
        # Create test data
        game_info = pd.DataFrame({'col1': [1]})
        team_stats = pd.DataFrame({'col1': [1]})
        player_stats = pd.DataFrame({
            'player': ['Patrick Mahomes'],
            'team': ['KAN'],
            'passing_yards': [300]
        })
        
        transformer = GamePageTransformer(game_info, team_stats, player_stats)
        
        # Test the transform method
        result = transformer.transform_player_stats_df()
        
        # Verify result is a dataframe
        assert isinstance(result, pd.DataFrame)
        assert not result.empty


if __name__ == "__main__":
    pytest.main([__file__])
    
    
