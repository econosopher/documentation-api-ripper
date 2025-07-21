// Swagger/OpenAPI YAML Extractor for Chrome Console
// This script extracts the raw API specification from Swagger UI pages

(async function extractSwaggerSpec() {
    console.log('🔍 Searching for Swagger/OpenAPI specification...\n');
    
    // Method 1: Check window.ui (most common in Swagger UI)
    if (window.ui && window.ui.specSelectors && window.ui.specSelectors.specJson) {
        try {
            const spec = window.ui.specSelectors.specJson();
            if (spec) {
                console.log('✅ Found spec in window.ui');
                console.log('📋 Copy the spec below:\n');
                console.log(JSON.stringify(spec, null, 2));
                return;
            }
        } catch (e) {
            console.log('❌ window.ui method failed:', e.message);
        }
    }
    
    // Method 2: Check for spec URL in the initialization
    const scripts = Array.from(document.querySelectorAll('script'));
    for (const script of scripts) {
        const content = script.textContent || '';
        
        // Look for common patterns
        const patterns = [
            /url:\s*["']([^"']*\.(yaml|yml|json))["']/i,
            /spec:\s*["']([^"']*\.(yaml|yml|json))["']/i,
            /configUrl:\s*["']([^"']*\.(yaml|yml|json))["']/i,
            /swaggerUrl:\s*["']([^"']*\.(yaml|yml|json))["']/i
        ];
        
        for (const pattern of patterns) {
            const match = content.match(pattern);
            if (match && match[1]) {
                console.log(`✅ Found spec URL: ${match[1]}`);
                
                // Resolve relative URLs
                const specUrl = new URL(match[1], window.location.href).href;
                
                try {
                    const response = await fetch(specUrl);
                    const contentType = response.headers.get('content-type') || '';
                    
                    if (contentType.includes('yaml') || contentType.includes('yml') || specUrl.match(/\.(yaml|yml)$/i)) {
                        const yaml = await response.text();
                        console.log('📋 Copy the YAML spec below:\n');
                        console.log(yaml);
                    } else {
                        const json = await response.json();
                        console.log('📋 Copy the JSON spec below:\n');
                        console.log(JSON.stringify(json, null, 2));
                    }
                    return;
                } catch (e) {
                    console.log(`❌ Failed to fetch ${specUrl}:`, e.message);
                }
            }
        }
    }
    
    // Method 3: Look for common API definition endpoints
    const commonPaths = [
        './openapi.yaml',
        './openapi.yml',
        './openapi.json',
        './swagger.yaml',
        './swagger.yml',
        './swagger.json',
        './api-docs',
        './v1/api-docs',
        './v2/api-docs',
        './v3/api-docs',
        '../openapi.yaml',
        '../openapi.json',
        '/openapi.yaml',
        '/openapi.json',
        '/swagger.json',
        '/api/swagger.json',
        '/api/openapi.json',
        // Additional paths for various API doc systems
        '/api/docs/*.yml',
        '/api/docs/*.yaml',
        '*.yml',
        '*.yaml',
        'docs/*.yml',
        'docs/*.yaml'
    ];
    
    console.log('🔍 Checking common spec locations...');
    
    for (const path of commonPaths) {
        try {
            const url = new URL(path, window.location.href).href;
            const response = await fetch(url, { method: 'HEAD' });
            
            if (response.ok) {
                console.log(`✅ Found spec at: ${url}`);
                const fullResponse = await fetch(url);
                const contentType = fullResponse.headers.get('content-type') || '';
                
                if (contentType.includes('yaml') || contentType.includes('yml') || url.match(/\.(yaml|yml)$/i)) {
                    const yaml = await fullResponse.text();
                    console.log('📋 Copy the YAML spec below:\n');
                    console.log(yaml);
                } else {
                    const json = await fullResponse.json();
                    console.log('📋 Copy the JSON spec below:\n');
                    console.log(JSON.stringify(json, null, 2));
                }
                return;
            }
        } catch (e) {
            // Silently continue to next path
        }
    }
    
    // Method 4: Check Network tab hint
    console.log('\n📡 Additional tips:');
    console.log('1. Open Network tab and refresh the page');
    console.log('2. Filter by "Doc" or search for ".yml", ".yaml", ".json"');
    console.log('3. Look for files like:');
    console.log('   - app_analysis.yml (Sensor Tower)');
    console.log('   - api-docs.json');
    console.log('   - openapi.yaml');
    console.log('4. Click the file → Response tab → Copy all content');
    console.log('5. Save to a file and convert with openapi_to_markdown.py');
    
    // Method 5: Extract from Swagger UI state
    if (window.SwaggerUIBundle || window.SwaggerUI) {
        console.log('\nℹ️ Swagger UI detected but couldn\'t extract spec automatically.');
        console.log('Try: window.ui.specSelectors.specJson() in console');
    }
})();