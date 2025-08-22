#!/usr/bin/env python3
"""
DOM Tree Extraction - Core Tree Extractor Module
Phase 3: Tree Expansion Algorithm
"""

from playwright.sync_api import Page
import json
import time
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TreeExtractor:
    def __init__(self, page: Page):
        self.page = page
        self.max_timeout = 60  # seconds
        self.start_time = time.time()
        self.expansion_attempts = 0
        self.max_expansion_attempts = 50
        
    def is_timeout_exceeded(self) -> bool:
        """Check if maximum timeout has been exceeded"""
        return (time.time() - self.start_time) > self.max_timeout
    
    def find_expandable_nodes(self) -> List[Any]:
        """Find all currently expandable (collapsed) nodes with prioritization"""
        try:
            # Look for various types of expandable nodes
            selectors = [
                '[aria-expanded="false"]',  # Standard ARIA pattern
                '[class*="chevron"][class*="right"]',  # Right-pointing chevrons
                '[class*="expand"][class*="collapsed"]',  # Collapsed expanders
                '[class*="tree-node"][class*="collapsed"]',  # Collapsed tree nodes
                '[class*="folder"][class*="closed"]',  # Closed folders
                'button[class*="expand"]',  # Expand buttons
                'span[class*="expand"]',  # Expand spans
                'div[class*="expand"]'  # Expand divs
            ]
            
            expandable_nodes = []
            for selector in selectors:
                try:
                    nodes = self.page.query_selector_all(selector)
                    expandable_nodes.extend(nodes)
                    if nodes:
                        logger.info(f"Found {len(nodes)} expandable nodes with selector: {selector}")
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            # Remove duplicates while preserving order
            seen = set()
            unique_nodes = []
            for node in expandable_nodes:
                node_id = id(node)
                if node_id not in seen:
                    seen.add(node_id)
                    unique_nodes.append(node)
            
            logger.info(f"Total unique expandable nodes found: {len(unique_nodes)}")
            
            # Prioritize nodes that are likely to contain document content
            prioritized_nodes = self._prioritize_nodes(unique_nodes)
            return prioritized_nodes
            
        except Exception as e:
            logger.error(f"Error finding expandable nodes: {e}")
            return []
    
    def _prioritize_nodes(self, nodes: List[Any]) -> List[Any]:
        """Prioritize nodes based on content importance for faster processing"""
        try:
            # Keywords that indicate important document content
            important_keywords = [
                'document', 'article', 'statute', 'rule', 'partnership',
                'association', 'register', 'legal', 'entity', 'business',
                'company', 'corporation', 'limited', 'gmbh', 'ag'
            ]
            
            prioritized = []
            regular = []
            
            for node in nodes:
                try:
                    node_text = node.text_content().lower() if node.text_content() else ""
                    
                    # Check if node contains important keywords
                    is_important = any(keyword in node_text for keyword in important_keywords)
                    
                    if is_important:
                        prioritized.append(node)
                    else:
                        regular.append(node)
                        
                except Exception:
                    # If we can't read the node, put it in regular priority
                    regular.append(node)
            
            # Return important nodes first, then regular ones
            result = prioritized + regular
            logger.info(f"Prioritized {len(prioritized)} important nodes out of {len(nodes)} total")
            
            return result
            
        except Exception as e:
            logger.error(f"Error prioritizing nodes: {e}")
            return nodes  # Return original list if prioritization fails
    
    def expand_node(self, node) -> bool:
        """Expand a single node and wait for content to load"""
        try:
            # Check if node is still expandable
            if not self.is_node_expandable(node):
                logger.debug("Node is no longer expandable, skipping")
                return False
            
            # Try different expansion methods
            expansion_methods = [
                self._click_expand,
                self._click_node,
                self._press_enter,
                self._double_click
            ]
            
            for method in expansion_methods:
                try:
                    if method(node):
                        logger.debug(f"Successfully expanded node using {method.__name__}")
                        return True
                except Exception as e:
                    logger.debug(f"Method {method.__name__} failed: {e}")
                    continue
            
            logger.warning("All expansion methods failed for node")
            return False
            
        except Exception as e:
            logger.error(f"Error expanding node: {e}")
            return False
    
    def _click_expand(self, node) -> bool:
        """Click on expand button/icon"""
        try:
            # Look for expand button within the node
            expand_button = node.query_selector('[class*="expand"], [class*="chevron"], button, span')
            if expand_button:
                expand_button.click()
                return self.wait_for_expansion()
            return False
        except Exception:
            return False
    
    def _click_node(self, node) -> bool:
        """Click on the node itself"""
        try:
            node.click()
            return self.wait_for_expansion()
        except Exception:
            return False
    
    def _press_enter(self, node) -> bool:
        """Press Enter key on the node"""
        try:
            node.focus()
            node.press('Enter')
            return self.wait_for_expansion()
        except Exception:
            return False
    
    def _double_click(self, node) -> bool:
        """Double-click on the node"""
        try:
            node.dblclick()
            return self.wait_for_expansion()
        except Exception:
            return False
    
    def is_node_expandable(self, node) -> bool:
        """Check if a node is still expandable"""
        try:
            # Check various indicators that the node is still collapsed
            indicators = [
                '[aria-expanded="false"]',
                '[class*="chevron"][class*="right"]',
                '[class*="collapsed"]',
                '[class*="closed"]'
            ]
            
            for indicator in indicators:
                if node.query_selector(indicator):
                    return True
            
            return False
        except Exception:
            return False
    
    def wait_for_expansion(self, timeout=5000) -> bool:
        """Wait for dynamic content to load after expansion"""
        try:
            # Wait for network to be idle
            self.page.wait_for_load_state('networkidle', timeout=timeout)
            
            # Additional wait for any animations to complete
            self.page.wait_for_timeout(200)
            
            return True
        except Exception as e:
            logger.debug(f"Wait timeout: {e}")
            return False
    
    def expand_all_nodes(self) -> None:
        """Iteratively expand all nodes until tree is fully expanded"""
        logger.info("Starting tree expansion process...")
        
        iteration = 0
        
        while (iteration < self.max_expansion_attempts and 
               not self.is_timeout_exceeded()):
            
            # Check time limit - leave buffer for tree building
            if (time.time() - self.start_time) >= 50:  # 50s limit for expansion
                logger.warning("Time limit approaching, stopping expansion")
                break
            
            # Find expandable nodes
            expandable_nodes = self.find_expandable_nodes()
            
            if not expandable_nodes:
                logger.info(f"No more expandable nodes found after {iteration} iterations")
                break
            
            logger.info(f"Iteration {iteration}: Found {len(expandable_nodes)} expandable nodes")
            
            # Expand each node (limit to prevent hanging)
            expanded_count = 0
            nodes_to_process = min(len(expandable_nodes), 5)  # Process max 5 nodes per iteration
            
            for i, node in enumerate(expandable_nodes[:nodes_to_process]):
                if self.is_timeout_exceeded():
                    break
                
                if self.expand_node(node):
                    expanded_count += 1
                    
                # Small delay between nodes to prevent overwhelming the page
                if i < nodes_to_process - 1:
                    time.sleep(0.1)
                    
            if expanded_count == 0:
                logger.warning("No nodes were successfully expanded, stopping")
                break
                
            iteration += 1
            
            # Reduced delay between iterations
            time.sleep(0.2)
        
        if iteration >= self.max_expansion_attempts:
            logger.warning("Max iterations reached during tree expansion")
        
        logger.info(f"Tree expansion completed after {iteration} iterations")
    
    def extract_node_data(self, element) -> Dict[str, Any]:
        """Extract label, href, and children from a node"""
        try:
            data = {}
            
            # Extract label text
            label_selectors = [
                '[class*="label"]',
                '[class*="title"]',
                '[class*="text"]',
                'span',
                'div'
            ]
            
            for selector in label_selectors:
                label_elem = element.query_selector(selector)
                if label_elem and label_elem.text_content().strip():
                    data['label'] = label_elem.text_content().strip()
                    break
            
            if not data.get('label'):
                data['label'] = element.text_content().strip()[:100]
            
            # Extract href if present
            link_elem = element.query_selector('a[href]')
            if link_elem:
                data['href'] = link_elem.get_attribute('href')
            
            # Check if node has children (is expandable)
            data['expandable'] = self.is_node_expandable(element)
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting node data: {e}")
            return {'label': 'Error extracting data', 'href': None, 'expandable': False}
    
    def find_child_nodes(self, parent_element) -> List[Any]:
        """Find child nodes of a parent element (optimized for speed)"""
        try:
            # Use faster, more targeted selectors
            child_selectors = [
                '> div',  # Direct div children (most common)
                '> span',  # Direct span children
                '> a',     # Direct link children
                '> li',    # List items
                '> p'      # Paragraphs
            ]
            
            children = []
            for selector in child_selectors:
                try:
                    child_nodes = parent_element.query_selector_all(selector)
                    children.extend(child_nodes)
                    
                    # Limit total children to prevent excessive processing
                    if len(children) >= 50:
                        logger.debug(f"Reached child limit (50), stopping search")
                        break
                        
                except Exception:
                    continue
            
            # Quick deduplication (limit to first 50)
            unique_children = []
            seen = set()
            for child in children[:50]:  # Hard limit
                child_id = id(child)
                if child_id not in seen and child_id != id(parent_element):
                    seen.add(child_id)
                    unique_children.append(child)
            
            logger.debug(f"Found {len(unique_children)} child nodes")
            return unique_children
            
        except Exception as e:
            logger.error(f"Error finding child nodes: {e}")
            return []
    
    def build_tree_structure(self) -> Dict[str, Any]:
        """Build the final JSON tree structure with time awareness"""
        logger.info("Building tree structure from expanded DOM...")
        
        try:
            # Check time remaining - leave buffer for processing
            time_remaining = self.max_timeout - (time.time() - self.start_time)
            if time_remaining < 10:
                logger.warning(f"Only {time_remaining:.1f}s remaining, building minimal tree")
                return self._build_minimal_tree()
            
            # Find the root container - try multiple selectors
            root_selectors = [
                '[class*="document-tree"]',
                '[class*="tree-root"]',
                '[class*="tree-container"]',
                '[role="tree"]',
                'body'  # Fallback to body if no specific container found
            ]
            
            root_container = None
            for selector in root_selectors:
                root_container = self.page.query_selector(selector)
                if root_container:
                    logger.info(f"Found root container with selector: {selector}")
                    break
            
            if not root_container:
                logger.warning("Could not find tree root container, using body")
                root_container = self.page.query_selector('body')
            
            if not root_container:
                raise Exception("Could not find any root container")
            
            # Build tree with time monitoring
            tree_data = self._extract_subtree_timed(root_container, time_remaining)
            
            # Validate the tree structure
            self._validate_tree_structure(tree_data)
            
            logger.info("Tree structure built successfully")
            return tree_data
            
        except Exception as e:
            logger.error(f"Error building tree structure: {e}")
            raise
    
    def _extract_subtree_timed(self, element, time_remaining: float) -> Dict[str, Any]:
        """Recursively extract tree structure from DOM element with time monitoring"""
        try:
            # Check if we're running out of time
            if time.time() - self.start_time > self.max_timeout - 5:
                logger.warning("Time limit approaching, returning partial tree")
                return {'label': 'Partial tree (time limit)', 'children': []}
            
            # Extract basic node information
            node_data = self.extract_node_data(element)
            
            # Find child nodes (limit to prevent deep recursion)
            children = []
            child_elements = self.find_child_nodes(element)
            
            # Limit children to prevent excessive processing
            max_children = 20  # Limit to prevent deep recursion
            child_elements = child_elements[:max_children]
            
            for i, child_element in enumerate(child_elements):
                try:
                    # Check time before processing each child
                    if time.time() - self.start_time > self.max_timeout - 3:
                        logger.warning("Time limit reached, stopping child processing")
                        break
                    
                    child_node = self._extract_subtree_timed(child_element, time_remaining)
                    if child_node:
                        children.append(child_node)
                        
                    # Add small delay to prevent overwhelming the page
                    if i < len(child_elements) - 1:
                        time.sleep(0.01)
                        
                except Exception as e:
                    logger.debug(f"Error extracting child node: {e}")
                    continue
            
            # Build the node structure
            node = {
                'label': node_data.get('label', ''),
                'href': node_data.get('href'),
                'expandable': node_data.get('expandable', False),
                'children': children
            }
            
            # Remove None values
            node = {k: v for k, v in node.items() if v is not None}
            
            return node
            
        except Exception as e:
            logger.error(f"Error extracting subtree: {e}")
            return {'label': 'Error extracting subtree', 'children': []}
    
    def _extract_subtree(self, element) -> Dict[str, Any]:
        """Legacy method - kept for compatibility"""
        return self._extract_subtree_timed(element, self.max_timeout)
    
    def _build_minimal_tree(self) -> Dict[str, Any]:
        """Build a minimal tree structure when time is limited"""
        logger.info("Building minimal tree structure due to time constraints")
        
        try:
            # Get basic page information
            title = self.page.title() or "German Business Register"
            
            # Find any visible text content
            body = self.page.query_selector('body')
            if body:
                text_content = body.text_content()[:200] + "..." if body.text_content() else "No content available"
            else:
                text_content = "No content available"
            
            # Create minimal tree
            minimal_tree = {
                'label': title,
                'href': self.page.url,
                'expandable': False,
                'children': [
                    {
                        'label': 'Page Content (Partial)',
                        'href': None,
                        'expandable': False,
                        'children': [
                            {
                                'label': text_content,
                                'href': None,
                                'expandable': False,
                                'children': []
                            }
                        ]
                    },
                    {
                        'label': 'Note: Tree extraction was limited due to time constraints',
                        'href': None,
                        'expandable': False,
                        'children': []
                    }
                ]
            }
            
            logger.info("Minimal tree built successfully")
            return minimal_tree
            
        except Exception as e:
            logger.error(f"Error building minimal tree: {e}")
            return {
                'label': 'Error: Could not build tree',
                'href': None,
                'expandable': False,
                'children': []
            }
    
    def _validate_tree_structure(self, tree_data: Dict[str, Any]) -> bool:
        """Validate the extracted tree structure"""
        try:
            def count_nodes(node):
                count = 1
                for child in node.get('children', []):
                    count += count_nodes(child)
                return count
            
            node_count = count_nodes(tree_data)
            logger.info(f"Extracted tree with {node_count} total nodes")
            
            # Validate required fields
            if not tree_data.get('label'):
                raise ValueError("Root node missing label")
            
            # Check for reasonable tree size
            if node_count < 1:
                raise ValueError("Tree must have at least one node")
            
            if node_count > 10000:  # Reasonable upper limit
                logger.warning(f"Very large tree detected: {node_count} nodes")
            
            return True
            
        except Exception as e:
            logger.error(f"Tree validation failed: {e}")
            raise
    
    def save_tree_to_file(self, tree_data: Dict[str, Any], filename: str = "output/extracted_tree.json") -> str:
        """Save the extracted tree to a JSON file"""
        try:
            import os
            os.makedirs("output", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tree_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Tree saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving tree to file: {e}")
            raise

def extract_tree_from_url(url: str, headless: bool = True) -> Dict[str, Any]:
    """Extract tree from a given URL using Playwright"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--headless'
            ]
        )
        page = browser.new_page()
        
        try:
            # Navigate to the page with faster wait strategy for 60s requirement
            page.goto(url, wait_until='commit', timeout=30000)  # 'commit' is faster than 'domcontentloaded'
            page.wait_for_load_state('domcontentloaded', timeout=15000)  # Reduced timeout
            
            # Extract tree
            extractor = TreeExtractor(page)
            extractor.expand_all_nodes()
            tree_data = extractor.build_tree_structure()
            
            return tree_data
            
        finally:
            browser.close()
