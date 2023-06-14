from .Class import BaseSLD


class Depth(BaseSLD):
    layerName = 'sea_depth'
    layerStyle = 'sea_depth'
    propertyName = 'z'
    depth = -15
    fill = '#0ACAB0'

    _vals = dict(
        layerName=layerName,
        layerStyle=layerStyle,
        propertyName=propertyName,
        depth=depth,
        fill=fill
    )

    def createSld(self):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
          xmlns:ogc="http://www.opengis.net/ogc"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld
         http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
          <NamedLayer>
            <Name>{self.layerName}</Name>
            <UserStyle>
              <FeatureTypeStyle>
                <Title>{self.layerStyle}</Title>
          

                
                <Rule>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>{self.propertyName}</ogc:PropertyName>
                            <ogc:Literal>{self.depth}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                
                
                    <PolygonSymbolizer>
                        <Fill>
                          <CssParameter name="fill">{self.fill}</CssParameter>
                        </Fill>

                    </PolygonSymbolizer>
                </Rule>
              </FeatureTypeStyle>
            </UserStyle>
          </NamedLayer>
        </StyledLayerDescriptor>
                """